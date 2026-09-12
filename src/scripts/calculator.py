import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from industrial_model.calculator import Calculator, CalculatorQuery
from industrial_model.models import InstanceId
from core import create_cognite_client

client = create_cognite_client()
calculator = Calculator(client)

from industrial_model.calculator import MultiTimeSeriesParameter  # noqa: E402

total_output = MultiTimeSeriesParameter(
    alias="IDT",
    timeseries_instance_ids=[
        InstanceId(
            space="sp_kpi_glb_dat",
            external_id="MCH-acea58aa17f237391294124100c22a28-parameter-IDT",
        ),
        InstanceId(
            space="sp_kpi_glb_dat",
            external_id="MCH-575f438522de1e6622d033f331257107-parameter-IDT",
        ),
        InstanceId(
            space="sp_kpi_glb_dat",
            external_id="MCH-128715a606a7a5cfbf6979c8f08555b8-parameter-IDT",
        ),
    ],
    aggregate_type="average",
    granularity="1m",
    reducer="average",
)
query = CalculatorQuery(
    formula="{IDT}",
    parameters=[total_output],
)
