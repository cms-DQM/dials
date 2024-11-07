#!/usr/bin/env python

from python.env import DATABASE_RUI
from python.models import DimMLModelsIndex
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker


def get_engine(workspace: str) -> Engine:
    return create_engine(f"{DATABASE_RUI}/{workspace}")


def register_model(ws, model_metadata):
    engine = get_engine(ws)
    Session = sessionmaker(bind=engine)  # noqa: N806
    with Session() as session:
        model = DimMLModelsIndex(
            filename=model_metadata["filename"],
            target_me=model_metadata["target_me"],
            active=model_metadata["active"],
        )
        session.add(model)
        session.commit()


if __name__ == "__main__":
    models = [
        {
            "filename": "model_CHFrac_highPt_Barrel_checkpoint_20240517.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_Barrel",
            "active": False,
        },
        {
            "filename": "model_CHFrac_highPt_EndCap_checkpoint_20240517.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_EndCap",
            "active": False,
        },
        {
            "filename": "model_CHFrac_lowPt_Barrel_checkpoint_20240517.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_Barrel",
            "active": False,
        },
        {
            "filename": "model_CHFrac_lowPt_EndCap_checkpoint_20240517.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_EndCap",
            "active": False,
        },
        {
            "filename": "model_CHFrac_mediumPt_Barrel_checkpoint_20240517.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_Barrel",
            "active": False,
        },
        {
            "filename": "model_CHFrac_mediumPt_EndCap_checkpoint_20240517.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_EndCap",
            "active": False,
        },
        {
            "filename": "model_MET_2_checkpoint_20240517.onnx",
            "target_me": "JetMET/MET/pfMETT1/Cleaned/MET_2",
            "active": False,
        },
        {
            "filename": "model_METPhi_checkpoint_20240517.onnx",
            "target_me": "JetMET/MET/pfMETT1/Cleaned/METPhi",
            "active": False,
        },
        {
            "filename": "model_METSig_checkpoint_20240517.onnx",
            "target_me": "JetMET/MET/pfMETT1/Cleaned/METSig",
            "active": False,
        },
        {
            "filename": "model_SumET_checkpoint_20240517.onnx",
            "target_me": "JetMET/MET/pfMETT1/Cleaned/SumET",
            "active": False,
        },
        {
            "filename": "model_CHFrac_highPt_Barrel_checkpoint_20240720.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_Barrel",
            "active": True,
        },
        {
            "filename": "model_CHFrac_highPt_EndCap_checkpoint_20240720.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_EndCap",
            "active": True,
        },
        {
            "filename": "model_CHFrac_lowPt_Barrel_checkpoint_20240720.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_Barrel",
            "active": True,
        },
        {
            "filename": "model_CHFrac_lowPt_EndCap_checkpoint_20240720.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_EndCap",
            "active": True,
        },
        {
            "filename": "model_CHFrac_mediumPt_Barrel_checkpoint_20240720.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_Barrel",
            "active": True,
        },
        {
            "filename": "model_CHFrac_mediumPt_EndCap_checkpoint_20240720.onnx",
            "target_me": "JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_EndCap",
            "active": True,
        },
        {
            "filename": "model_MET_2_checkpoint_20240720.onnx",
            "target_me": "JetMET/MET/pfMETT1/Cleaned/MET_2",
            "active": True,
        },
        {
            "filename": "model_METPhi_checkpoint_20240720.onnx",
            "target_me": "JetMET/MET/pfMETT1/Cleaned/METPhi",
            "active": True,
        },
        {
            "filename": "model_METSig_checkpoint_20240720.onnx",
            "target_me": "JetMET/MET/pfMETT1/Cleaned/METSig",
            "active": True,
        },
        {
            "filename": "model_SumET_checkpoint_20240720.onnx",
            "target_me": "JetMET/MET/pfMETT1/Cleaned/SumET",
            "active": True,
        },
    ]
    for model_metadata in models:
        register_model("jetmet", model_metadata)
