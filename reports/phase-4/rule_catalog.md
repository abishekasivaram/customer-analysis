# Rule Catalog Documentation

| Rule Name | Purpose | Input Metrics | Thresholds | Generated Recommendation | Priority | Expected Output |
|-----------|---------|---------------|------------|--------------------------|----------|-----------------|
| CriticalCongestion | Detect severe bottlenecks | peak_occupancy | congestion.critical | Aisle widening | High | Reduce bottleneck |
| WarningCongestion | Detect moderate traffic | peak_occupancy | congestion.warning | Monitor layout | Medium | Prevent bottlenecks |
| HighTrafficLowInteraction | Find low product visibility | interaction_count, visitors | interaction.low | Relocate products | Medium | Higher visibility |
| HighInteractionLowConversion | Find strong engagement but low sales | interaction_rate | interaction.high | Promo campaigns | High | Convert sales |
| HighDwellLowInteraction | Find hesitation points | average_dwell_time, interaction_rate | dwell_time.high, interaction.low | Improve pricing/promos | Medium | Clear hesitation |
| LowCustomerFlow | Detect dead zones | dead_zones array | > 0 | Re-route traffic | Medium | Balance traffic |
