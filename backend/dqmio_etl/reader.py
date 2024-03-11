"""
**Class for reading DQMIO files and extracting histograms**

Originally copied from here: https://github.com/cms-DQM/ML4DQM-DC_SharedTools/blob/master/dqmio/moredqmiodata.ipynb

Notes:
* Should import root_numpy (efficient interface between ROOT and numpy), but it is not available on SWAN
* fnmatch provides support for unix shell-style wildcards, which are not the same as regular expressions in python
"""

import logging
from collections import defaultdict, namedtuple
from fnmatch import fnmatch
from multiprocessing.pool import ThreadPool
from typing import List, Optional

import ROOT

logger = logging.getLogger(__name__)


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

    TREE_NAMES = {
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

    def __init__(self, *files, **kwargs):
        """
        During class construction, open the passed in files and read their index data

        - files: a filename (or multiple filenames) to open
                 if stored locally, the filenames should contain the full path.
                 if stored on the grid, prefix the file path with "root://cms-xrd-global.cern.ch/"
        - kwargs:
            - nthreads: int (default 4) for number of threads
        """
        self.nthreads = int(kwargs.get("nthreads", 4))

        logger.debug(f"DQMIOReader.__init__: opening {len(files)} files...")
        self.rootfiles = [ROOT.TFile.Open(fp) for fp in files]
        logger.debug("DQMIOReader.__init__: All files opened, now making index...")
        self.__read_index_tables()
        logger.debug("DQMIOReader.__init__: List of monitored elements made.")

    def __get_me_type(self, metype):
        """
        Convert integer monitoring element type to string representation
        * the string representation must correspond to the directory structure in a DQMIO file!
        """
        return self.TREE_NAMES[metype]

    def __read_file_index(self, f):
        """
        Read file index from one file
        """
        # idx_tree = getattr(f, "Indices")
        idx_tree = f.Indices

        for i in range(idx_tree.GetEntries()):
            idx_tree.GetEntry(i)
            # get run number, lumi number, and type of monitoring element for this entry.
            # note: apparently idxtree contains one "entry" per run, lumisection and type;
            #       that is: all monitoring elements of the same type (e.g. TH1F) and for the same lumisection
            #       are in the same "entry"; this is what FirstIndex and LastIndex are for (see below).
            # note: apparently idxtree.Lumi gives 0 for per-run monitoring elements,
            #       but for now we ignore those and only read per-ls monitoring elements.
            run, lumi, metype = idx_tree.Run, idx_tree.Lumi, idx_tree.Type
            if lumi == 0:
                continue

            first_idx, lastidx = idx_tree.FirstIndex, idx_tree.LastIndex
            entry = DQMIOReader.IndexEntry(run, lumi, metype, f, first_idx, lastidx)
            self.index[(run, lumi)].append(entry)

    def __read_index_tables(self):
        """
        Read index tables
        * for internal use in initializer only, do not call.
        """
        self.index = defaultdict(list)
        self.index_keys = []

        # Reach index of each root file
        p = ThreadPool(self.nthreads)
        p.map(self.__read_file_index, self.rootfiles)
        p.close()

        # convert the defaultdict to a regular dict
        # (else unwanted behaviour when trying to retrieve lumisections that are not present;
        # in case of defaultdict they are added to the index as empty lists of IndexEntries)
        self.index = dict(self.index)
        self.index_keys = list(self.index.keys())

    def __extract_data_from_ROOT(self, root_obj, hist2array=False):
        """
        Extract ROOT-type data into useful formats, depending on the data type

        - root_obj: a ROOT object
        - hist2array: boolean whether to convert ROOT histograms to numpy arrays
                      (default: keep as ROOT histogram objects)
                      note: option True is not yet supported (need to fix root_numpy import in SWAN)
        """
        if isinstance(root_obj, (int, float)):
            return root_obj

        if hist2array:
            raise NotImplementedError(
                "ERROR in DQMIOReader.__extract_data_from_ROOT: option hist2array is not yet supported"
            )

        return root_obj.Clone()

    @staticmethod
    def __is_me_name_matching_selections(me_name, name_patterns):
        """
        Check if a monitoring element name matches required selections
        """
        for pattern in name_patterns:
            if fnmatch(me_name, pattern):
                return True
        return False

    def list_lumis(self):
        """
        Returns a list of (run number, lumisection number) pairs for the lumis available in the files.

        warning: copying the list is avoided to for speed and memory;
                 only meant for reading; if you want to modify the result, make a copy first!
        """
        return self.index_keys

    def get_mes_for_lumi(self, run, lumi, *name_patterns):
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
                if not self.__is_me_name_matching_selections(me_name, name_patterns):
                    continue

                me_tree.GetEntry(x, 1)
                value = me_tree.Value
                value = self.__extract_data_from_ROOT(value)
                me = self.MonitorElement(run, lumi, me_name, entry.type, value)
                result.append(me)

        return result

    def count_mes(self, whitelist_mes: Optional[List] = None, me_selection=(3, 4, 5, 6, 7, 8)):
        """
        Count how many monitoring elements exists given ME selection
        """
        num_total_entries = 0
        for run, lumi in self.list_lumis():
            melist = self.get_mes_for_lumi(run, lumi, "*")
            for me in melist:
                if whitelist_mes and me.name not in whitelist_mes:
                    continue
                if me.type in me_selection:
                    num_total_entries += 1
        return num_total_entries
