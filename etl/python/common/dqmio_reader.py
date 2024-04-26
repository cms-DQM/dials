"""
**Class for reading DQMIO files and extracting histograms**

Originally copied from here: https://github.com/cms-DQM/ML4DQM-DC_SharedTools/blob/master/dqmio/moredqmiodata.ipynb

Notes:
* Should import root_numpy (efficient interface between ROOT and numpy), but it is not available on SWAN
* fnmatch provides support for unix shell-style wildcards, which are not the same as regular expressions in python
"""

import re
from collections import defaultdict, namedtuple
from typing import ClassVar

import ROOT


class DQMIOReader:
    """
    Class for reading DQMIO input files and extracting histograms

    Attributes:
        - rootfiles: a list of root files (DQMIO format), opened in read mode
        - index: defaultdict matching tuples of the form (run number, lumisection number) to lists of IndexEntries.
                for each key of the form (run number, lumisection number), the value is a list of a few IndexEntries,
                one for each monitoring element type (so 12 at maximum).
                and empty list is returned from the dict if a given (run number, lumisection number) is not present.
        - indexlist: separate list of index keys for sortability in python2.
        - medict: dict containing all available monitor element names matched to their type.
        - melist: separate list of medict keys for sortabiltiy in python2.
        - nthreads: number of threads for multithreaded processing.
    """

    IndexEntry = namedtuple("IndexEntry", ["run", "lumi", "type", "file", "firstidx", "lastidx"])
    # an instance of IndexEntry represents one "entry" in a DQMIO file.
    # this "entry" corresponds to a single lumisection (characterized by run and lumi)
    # and a single type (e.g. TH1F, TH2F, etc.).
    # so all monitoring elements for this lumisection and for this type are in the same IndexEntry,
    # numbered from firstidx to lastidx.
    # note: the firstidx to lastidx range runs in parallel for multiple types (as they are stored in different trees);
    #       so multiple IndexEntries for the same lumisection (but different type) can have overlapping indices,
    #       but multiple IndexEntries for the same type and file but different lumisections have disjoint indices!

    MonitorElement = namedtuple("MonitorElement", ["run", "lumi", "name", "type", "data"])
    # an instance of MonitorElement represents one monitor element, with all associated information:
    # - the run and lumisection number
    # - the full name of the monitoring element
    # - the type (e.g. TH1F, TH2F, etc., see function __get_me_type below for all allowed types)
    # - the actual data

    TREE_NAMES: ClassVar[dict[int, str]] = {
        0: "Ints",
        1: "Floats",
        2: "Strings",
        3: "TH1Fs",
        4: "TH1Ss",
        5: "TH1Ds",
        6: "TH2Fs",
        7: "TH2Ss",
        8: "TH2Ds",
        9: "TH3Fs",
        10: "TProfiles",
        11: "TProfile2Ds",
    }

    def __init__(self, fpath: str) -> None:
        self.file = ROOT.TFile.Open(fpath)
        self.__read_index_tables()

    def __get_me_type(self, me_type):
        """
        Convert integer monitoring element type to string representation
        * the string representation must correspond to the directory structure in a DQMIO file!
        """
        return self.TREE_NAMES[me_type]

    def __read_file_index(self, f):
        """
        Read file index from one file
        """
        idx_tree = f.Indices

        for i in range(idx_tree.GetEntries()):
            idx_tree.GetEntry(i)
            # get run number, lumi number, and type of monitoring element for this entry.
            # note: apparently idxtree contains one "entry" per run, lumisection and type;
            #       that is: all monitoring elements of the same type (e.g. TH1F) and for the same lumisection
            #       are in the same "entry"; this is what FirstIndex and LastIndex are for (see below).
            # note: apparently idxtree.Lumi gives 0 for per-run monitoring elements,
            #       but for now we ignore those and only read per-ls monitoring elements.
            run, lumi, me_type = idx_tree.Run, idx_tree.Lumi, idx_tree.Type
            if lumi == 0:
                continue

            first_idx, lastidx = idx_tree.FirstIndex, idx_tree.LastIndex
            entry = DQMIOReader.IndexEntry(run, lumi, me_type, f, first_idx, lastidx)
            self.index[(run, lumi)].append(entry)

    def __read_index_tables(self):
        """
        Read index tables
        * for internal use in initializer only, do not call.
        """
        self.index = defaultdict(list)
        self.index_keys = []
        self.__read_file_index(self.file)

        # convert the defaultdict to a regular dict
        # (else unwanted behavior when trying to retrieve lumisections that are not present;
        # in case of defaultdict they are added to the index as empty lists of IndexEntries)
        self.index = dict(self.index)
        self.index_keys = [(run, lumi, int(self.cantor_pairing(run, lumi))) for run, lumi in self.index.keys()]

    def get_mes_for_lumi(self, run: int, lumi: int, types: tuple | list | None = None, re_pattern: str | None = None):
        """
        Get selected monitoring elements for a given lumisection

        args:
        - run: run number
        - lumi: lumisection number
        - namepatterns: a wildcard pattern (or multiple) to select monitoring elements

        returns:
        - a list of named tuples of type MonitorElement
        """
        runlumi = (run, lumi)

        # Get the data for the requested lumisection
        entries = self.index.get(runlumi, None)
        if entries is None:
            raise IndexError(
                f"ERROR in DQMIOReader.get_mes_for_lumi: requested to read data for lumisection {runlumi}"
                ", but no data was found for this lumisection in the current DQMIOReader."
            )

        # loop over all entries for this lumisection;
        # this corresponds to looping over all types of monitoring elements
        # (see the documentation of IndexEntry for more info).
        result = []
        for entry in entries:
            if types is not None and entry.type not in types:
                continue

            # read the correct tree from the file corresponding to this type of monitoring element
            me_attr_name = self.__get_me_type(entry.type)
            me_tree = getattr(entry.file, me_attr_name)
            me_tree.GetEntry(0)

            # disable all branches except "FullName"
            me_tree.SetBranchStatus("*", 0)
            me_tree.SetBranchStatus("FullName", 1)

            # loop over entries for this tree
            for x in range(entry.firstidx, entry.lastidx + 1):
                me_tree.GetEntry(x)
                me_name = str(me_tree.FullName)  # extract the monitoring element name and check if it is needed
                if re_pattern is not None and not re.search(re_pattern, me_name):
                    continue

                me_tree.GetEntry(x, 1)
                value = me_tree.Value.Clone()
                me = self.MonitorElement(run, lumi, me_name, entry.type, value)
                result.append(me)

        return result

    def close(self):
        self.file.Close()

    @staticmethod
    def th1_from_cppyy(me: "MonitorElement") -> dict:
        me_name = me.name
        entries = int(me.data.GetEntries())
        hist_x_bins = int(me.data.GetNbinsX())
        hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
        hist_x_max = me.data.GetXaxis().GetBinLowEdge(hist_x_bins + 1)  # Takes low edge of overflow bin instead.
        data = [me.data.GetBinContent(i) for i in range(1, hist_x_bins + 1)]
        return {
            "me": me_name,
            "x_min": hist_x_min,
            "x_max": hist_x_max,
            "x_bin": hist_x_bins,
            "entries": entries,
            "data": data,
        }

    @staticmethod
    def th2_from_cppyy(me: "MonitorElement") -> dict:
        me_name = me.name
        entries = int(me.data.GetEntries())
        hist_x_bins = int(me.data.GetNbinsX())
        hist_y_bins = int(me.data.GetNbinsY())
        hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
        hist_x_max = me.data.GetXaxis().GetBinLowEdge(hist_x_bins) + me.data.GetXaxis().GetBinWidth(hist_x_bins)
        hist_y_min = me.data.GetYaxis().GetBinLowEdge(1)
        hist_y_max = me.data.GetYaxis().GetBinLowEdge(hist_y_bins) + me.data.GetYaxis().GetBinWidth(hist_y_bins)

        # data should be in the form of data[x][y]
        data = [[me.data.GetBinContent(j, i) for j in range(1, hist_x_bins + 1)] for i in range(1, hist_y_bins + 1)]

        return {
            "me": me_name,
            "x_min": hist_x_min,
            "x_max": hist_x_max,
            "x_bin": hist_x_bins,
            "y_min": hist_y_min,
            "y_max": hist_y_max,
            "y_bin": hist_y_bins,
            "entries": entries,
            "data": data,
        }

    @staticmethod
    def cantor_pairing(x, y):
        return 0.5 * (x + y) * (x + y + 1) + y
