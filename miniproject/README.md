# Digital Equity Index

## Project Files

### original_broadband_data.json

This file contains the raw broadband and mobile connectivity data for each region. The indicators used collectively represent different dimensions of digital infrastructure and digital accessibility, which together contribute to the Digital Equity Index.

### weights.json

This file contains the weights assigned to each indicator. The weights represent the relative importance of each indicator in the calculation of the Digital Equity Index and must sum to:

Σ Weight = 1

### Digital_equity_Index.py

This Python script performs the complete index calculation process.

#### Inputs

* `original_broadband_data.json`
* `weights.json`

#### Processing

The script first normalizes all indicators to a common scale between 0 and 1.

For indicators where higher values indicate better performance:

Normalized Value = Actual Value / Maximum Value

For indicators where lower values indicate better performance:

Normalized Value = (1 − Actual Value) / (1 − Minimum Value)

The normalized values are then multiplied by their corresponding weights:

Weighted Score = Normalized Value × Weight

Finally, the Digital Equity Index is calculated as:

Digital Equity Index = Σ (Normalized Value × Weight)

Since all normalized values lie between 0 and 1 and the weights sum to 1, the resulting index is also bounded between 0 and 1.

#### Outputs

* `normalized_broadband_data.json`
* `weighted_normalized_broadband_data.json`

### normalized_broadband_data.json

This intermediate output file contains the normalized values for each indicator after the normalization process has been completed, but before weights are applied. All indicator values are transformed onto a common scale between 0 and 1, allowing indicators with different units and ranges to be compared consistently.

### weighted_normalized_broadband_data.json

This final output file contains the normalized values, weighted values, and final Digital Equity Index score for each region. The index represents the weighted aggregation of all normalized indicators and provides a single measure of digital equity for comparative analysis across regions.
