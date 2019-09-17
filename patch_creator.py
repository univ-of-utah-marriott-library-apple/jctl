#!/usr/bin/python

def xml_from_dict(data, string=None):
    """
    recursively builds xml document from provided dictionary
    """
    # self.logger.info("%s: activated" % inspect.stack()[0][3])
    xml_string = string or ''
        
    if isinstance(data, list):
        for item in data:
            xml_string = xml_from_dict(item, xml_string)
    elif isinstance(data, dict):
        for key, value in data.items():
            xml_string = xml_string + ("<%s>" % key)
            xml_string = xml_from_dict(value, xml_string)
            xml_string = xml_string + ("</%s>" % key)
    else:
        if isinstance(data, bool):
            data = str(data).lower()
        
        xml_string = xml_string + ("%s" % data)
    
    return xml_string


def main():
    appname = 'Compressor'
    icon_id = 1697 #Compressor

    version = {'latest': '4.4.4',
               'beta': '4.4.4',
               'stable': '4.4.4'}

    # policy templates
    policies = [{'name': 'Tech - Test Boxes',
                 'method': 'prompt',
                 'version': version['latest'],
                 'group': 'Staging - Tech Box'},
                {'name': 'Tech - Main Boxes',
                 'method': 'selfservice',
                 'defer': 3,
                 'version': version['latest'],
                 'grace': 60,
                 'group': 'Staging - Admin Tech'},
                {'name': 'Guinea Pig - Lab',
                 'method': 'prompt',
                 'version': version['beta'],
                 'group': 'Staging - Guinea Pig - Lab'},
                {'name': 'Guinea Pig - Staff',
                 'method': 'selfservice',
                 'version': version['beta'],
                 'defer': 7,
                 'grace': 60,
                 'group': 'Staging - Guinea Pig - Staff'},
                {'name': 'Stable - Lab',
                 'version': version['stable'],
                 'method': 'prompt',
                 'group': 'Staging - Stable - Lab'},
                {'name': 'Stable - Staff',
                 'method': 'selfservice',
                 'version': version['stable'],
                 'defer': 7,
                 'grace': 60,
                 'group': 'Staging - Stable - Staff'}]

    grace = {'grace_period_duration': 15,
             'notification_center_subject': 'Important',
             'message': ('$APP_NAMES will quit in $DELAY_MINUTES minutes so'
                         ' that $SOFTWARE_TITLE can be updated. Save anything'
                         ' you are working on and quit the app(s)')}
    
    for p in policies:
        name = p['name'] + ' - ' + appname
        # general
        general = {'name': name,
                   'target_version': p['version'],
                   'enabled': True,
                   'distribution_method': p['method'],
                   'allow_downgrade': False,
                   'patch_unknown': False}
        # scoping
        scope = {'computer_groups': {'computer_group': {'name': p['group']}}}

        _grace = grace.copy()
        _grace['grace_period_duration'] = p.get('grace', 15)
        data = {'patch_policy': {'general': general, 'scope': scope}}
        
        # Dynamic Notification
        if ('Main' in name) or ('Staff' in name):
            # Self Service
            deferal = p.get('defer', 7)
            interaction = {'install_button_text': 'Update',
                           'self_service_icon': {'id': icon_id},
                           'notifications': {'notification_enabled': True,
                                             'notification_type': 'Self Service',
                                             'notification_subject': 'update available',
                                             'notification_message': "This update will be installed automatically after {0!s} days.".format(deferal),
                                             'reminders': {'notification_reminders_enabled': True,
                                                           'notification_reminder_frequency': 1}},
                                             'deadlines': {'deadline_enabled': True,
                                                           'deadline_period': deferal},
                                             'grace_period': _grace}
        
        print(xml_from_dict(data))
        break
        print('\n'+'-'*79+'\n')
    
    

if __name__ == '__main__':
    main()