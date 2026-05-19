def clean_raw_name(name: str) -> str:
    return (
        name.strip()
        .rsplit(" ", 1)[0]
        .strip()
    )