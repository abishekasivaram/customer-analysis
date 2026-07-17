# Store Health Formula Documentation

## Scoring Equation
Base Score = 100.0
Score = Base Score - Penalties + Rewards

## Weights and Normalization
1. **Congestion Index Penalty**:
   - If congestion > 80: -20 points
   - If congestion > 50: -10 points
2. **Engagement Score Reward/Penalty**:
   - If engagement > 80: +0 points (no penalty)
   - If engagement < 40: -15 points
3. **Dead Zone Penalty**:
   - -5 points per dead zone detected

## Bounds
Maximum Score = 100.0
Minimum Score = 0.0

## Worked Numerical Example
- Base: 100
- Congestion Index is 90 (> 80): Penalty = -20
- Engagement Score is 30 (< 40): Penalty = -15
- 2 Dead Zones: Penalty = 2 * -5 = -10
**Final Score** = 100 - 20 - 15 - 10 = 55.0
