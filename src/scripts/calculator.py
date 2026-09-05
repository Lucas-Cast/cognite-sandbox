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
        InstanceId(space="plant", external_id="ts_line_1"),
        InstanceId(space="plant", external_id="ts_line_2"),
        InstanceId(space="plant", external_id="ts_line_3"),
    ],
    aggregate_type="sum",
    granularity="1m",
    reducer="sum",
)
query = CalculatorQuery(
    formula="{IDT}",
    parameters=[total_output],
)
