def update_streak(category, healthy_streak, junk_streak):

    # ensure streak values are integers
    healthy_streak = int(healthy_streak)
    junk_streak = int(junk_streak)

    if category == "Healthy":
        healthy_streak += 1
        junk_streak = 0

    elif category == "Junk":
        junk_streak += 1
        healthy_streak = 0

    elif category == "Moderate":
        # Moderate food breaks both streaks
        healthy_streak = 0
        junk_streak = 0

    return healthy_streak, junk_streak