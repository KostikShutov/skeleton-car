from dotenv import dotenv_values


def mergeEnvs(firstConfig: dict, secondConfig: dict) -> dict:
    result = firstConfig.copy()
    result.update(secondConfig)
    return result


env: dict = mergeEnvs(
    dotenv_values('.env'),
    dotenv_values('.env.local'),
)
