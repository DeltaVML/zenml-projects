import pandas as pd
import requests
from evidently.model_profile import Profile  # type: ignore
from zenml.steps import step
import json

# This is a private ZenML Discord channel. We will get notified if you use
# this, but you won't be able to see it. Feel free to create a new Discord
# [webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
# and replace this one!
DISCORD_URL = (
    "https://discord.com/api/webhooks/935835443826659339/Q32jTwmqc"
    "GJAUr-r_J3ouO-zkNQPchJHqTuwJ7dK4wiFzawT2Gu97f6ACt58UKFCxEO9"
)


@step(enable_cache=False)
def discord_alert(
    datadrift: str,
) -> bool:
    """Send a message to the discord channel to report drift.

    Args:
        datadrift: The drift report generated by evidently
    """
    drift = json.loads(datadrift)["metrics"][0]["result"]["dataset_drift"]
    url = DISCORD_URL
    data = {
        "content": "Drift Detected!" if drift else "No Drift Detected!",
        "username": "Drift Bot",
    }
    result = requests.post(url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(
            "Posted to discord successfully, code {}.".format(
                result.status_code
            )
        )
    print("Drift detected" if drift else "No Drift detected")
    return drift


@step(enable_cache=False)
def discord_post_prediction(
    prediction: pd.DataFrame,
) -> None:
    """Send a message to the discord channel to report the prediction
    for the upcoming nba game.

    Args:
        prediction: Table containing the prediction for the next weeks games
    """
    url = DISCORD_URL
    game = prediction.iloc[0]
    prediction_message = (
        f"On {game.name}, {game.Home_Team} will be facing off "
        f"against {game.Away_Team}. Something tells me that "
        f"{game.Home_Team}  will throw "
        f"{game.Predicted_3_Pointers_Home_Team:.1f} "
        f"three pointers"
    )
    data = {"content": prediction_message, "username": "Prediction Bot"}
    result = requests.post(url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(
            "Posted to discord successfully, code {}.".format(
                result.status_code
            )
        )
    print(prediction_message)
    return
