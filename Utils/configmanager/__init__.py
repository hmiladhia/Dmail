from Utils.configmanager._configmanager import ConfigManager


def hello(*args, **kwargs):
    print(kwargs)


if __name__ == "__main__":
    cm = ConfigManager('../../DemEmail/config')
    # from config import GmailConfig
    #
    # gmailConfig = GmailConfig()
    # cm.export_config(gmailConfig)

    conf = cm.load_config('TestConfig')
    print(conf.__dict__)
    print(conf.mail_port)
    print(conf.get_name())
    # hello(**conf)
