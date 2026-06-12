# Digital Equity Index

## Files in this project

### `BroadbandDashboardDataFile.xlsx`
Contains the original broadband dataset downloaded from external sources. This file includes the raw sub-constituency-level broadband indicators before any normalization or weighting has been applied.

### `normalized_subconstituency_data.xlsx`
Contains the sub-constituency data after normalization. All indicator values have been transformed onto a common 0–1 scale and are ready for index calculation.

### `weights_with_speed.json`
Contains the weights used when average download speed is included in the Digital Equity Index.

### `weights_without_speed.json`
Contains the weights used when average download speed is excluded from the Digital Equity Index.

### `weighted_parameters_with_speed.xlsx`
Contains the normalized values, weighted values, and Digital Equity Index for each sub-constituency using the weight set that includes average download speed.

### `weighted_parameters_without_speed.xlsx`
Contains the normalized values, weighted values, and Digital Equity Index for each sub-constituency using the weight set that excludes average download speed.

### `digital_equity_index_with_speed.xlsx`
Contains the final Digital Equity Index values for each sub-constituency using the weight set that includes average download speed.

### `digital_equity_index_without_speed.xlsx`
Contains the final Digital Equity Index values for each sub-constituency using the weight set that excludes average download speed.

### `digital_equity_index_with_speed.png`
A plot of the Digital Equity Index values for all sub-constituencies when average download speed is included. Index values are displayed in descending order.

### `digital_equity_index_without_speed.png`
A plot of the Digital Equity Index values for all sub-constituencies when average download speed is excluded. Index values are displayed in descending order.

---

## What the code does

`Digital_Equity_Index.py` reads:

- `normalized_subconstituency_data.xlsx`
- `weights_with_speed.json`
- `weights_without_speed.json`

The code multiplies each normalized indicator by its corresponding weight and sums the weighted values to calculate a Digital Equity Index for each sub-constituency.

The code outputs:

- `weighted_parameters_with_speed.xlsx`
- `weighted_parameters_without_speed.xlsx`
- `digital_equity_index_with_speed.xlsx`
- `digital_equity_index_without_speed.xlsx`
- `digital_equity_index_with_speed.png`
- `digital_equity_index_without_speed.png`

Two sets of results are produced because the project compares Digital Equity Index values with and without average download speed as an indicator. This allows the analysis to assess the influence of average download speed on sub-constituency rankings and overall index outcomes.

The original dataset (`BroadbandDashboardDataFile.xlsx`) is not processed directly by the current version of the code. An earlier version of the workflow was used to normalize the raw broadband indicators and generate `normalized_subconstituency_data.xlsx`. This approach was adopted because processing and normalizing the original dataset within the current code resulted in significantly slower execution times. Using the pre-normalized dataset allows the index calculation and visualisation stages to run much more efficiently.