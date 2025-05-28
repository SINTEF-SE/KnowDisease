from pydantic import BaseModel, Field, constr

class DiseaseTheorySchema(BaseModel):
    disease_name: str = Field(
        description="Disease, condition, syndrome, illness name"
    )
    etiology_factor: constr(max_length=1500) = Field(
        description="Cause, trigger, mutation, infection, exposure, origin"
    )
    diagnostic_method: constr(max_length=1500) = Field(
        description="Diagnosis, test, procedure, imaging, biopsy, criteria"
    )
    biomarker: constr(max_length=1500) = Field(
        description="Biomarker, indicator, gene, protein, measurement, state, progression, response"
    )
    treatment_intervention: constr(max_length=1500) = Field(
        description="Treatment, therapy, drug, surgery, intervention, management"
    )
    prognostic_indicator: constr(max_length=1500) = Field(
        description="Prognosis, outcome, survival, predictor, factor, metric"
    )