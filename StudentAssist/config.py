import os
import json
import logging

log = logging.getLogger()

# LUT for the logging config option.
LOGGING_LUT = {
    "DEBUG" : logging.DEBUG,
    "INFO" : logging.INFO,
    "WARNING" : logging.WARNING,
    "ERROR" : logging.ERROR,
    "CRITICAL" : logging.CRITICAL}


config_file = "StudentAssist/config.json"

def generate_config():
    log.info("Attemping to create config file at: " + config_file)
    with open(config_file, "w") as cfg:
        # Populate the config with a skeleton of the config
        config_contents = {"StudentAssist" : {
                                    "database" : {"path" : "StudentAssist/database/StudentAssist.db"},
                                    "logging" : {"logLevel" : "INFO", "logToFile" : False, "logPath" : ""}}}
        
        cfg.writelines(json.dumps(config_contents, indent=2))

def read_config():
    log.info("Attempting to read config file: " + config_file)
    with open(config_file, "r") as cfg:
        sa_cfg = json.loads(cfg.read())
    
    return sa_cfg

def write_config(sa_cfg):
    log.info("Attempting to write to config file: " + config_file)
    full_config = {"StudentAssist" : sa_cfg}
    with open(config_file, "w") as cfg:
        cfg.write(json.dumps(full_config, indent=2))

if not os.path.isfile(config_file):
    generate_config()

# Open the JSON config file and read it
try:
    sa_cfg = read_config()["StudentAssist"]
except KeyError:
    log.error("Invalid configuration file! \"StudentAssist\" key not found!")
    exit()


# Get the logging object associated with the provided string and set it.
if sa_cfg.get("logging").get("logLevel") in LOGGING_LUT:
    sa_cfg["logging"]["logLevel"] = LOGGING_LUT.get(sa_cfg.get("logging").get("logLevel"))
    log.info("Logging level set to: " + str(sa_cfg.get("logging").get("logLevel")))
else:
    log.info("No valid log level found in \"" + config_file + "\", defaulting to INFO.")
    sa_cfg["logging"]["logLevel"] = LOGGING_LUT.get("INFO")

if __name__ == "__main__":
    print(sa_cfg)