"""
This module contains the reward function for the validator.
"""

import bittensor as bt

RATE_OF_RECOVERY = 0.2
RATE_OF_DECAY = 0.4

MINIMUM_SCORE = 0

RESPONSE_TIME_WEIGHT = 0.2
PROOF_SIZE_WEIGHT = 0.1

RESPONSE_TIME_THRESHOLD = 240
PROOF_SIZE_THRESHOLD = 30000


def reward(max_score, score, value, response_time, proof_size):
    """
    This function calculates the reward for a miner based on the provided score, value, response time and proof size.
    Positional Arguments:
        max_score (int): The maximum score for the miner.
        score (int): The current score for the miner.
        value (bool): Whether the response that the miner submitted was valid.
        response_time (float): The time taken to respond to the query.
        proof_size (int): The size of the proof.
    Returns:
        int: The new score for the miner.
    """
    rate = RATE_OF_DECAY
    distance = score - MINIMUM_SCORE
    if value:
        bt.logging.trace(f"Recovering score {score}")
        performance_metric = (
            1
            - RESPONSE_TIME_WEIGHT * min(1, response_time / RESPONSE_TIME_THRESHOLD)
            - PROOF_SIZE_WEIGHT * min(1, proof_size / PROOF_SIZE_THRESHOLD)
        )

        rate = RATE_OF_RECOVERY * performance_metric
        distance = max_score - score
        return min(
            1,
            max(0, score + rate * distance - (1 - performance_metric) * 0.005),
        )

    bt.logging.trace(f"Decaying score {score}")
    return score - rate * distance
