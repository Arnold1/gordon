from troposphere import cloudformation, Join, Ref
from gordon.utils import valid_cloudformation_name


class BaseLambdaAWSCustomObject(cloudformation.AWSCustomObject):

    lambda_name = 'gordon_contrib_utils_sleep'

    @classmethod
    def create_with(cls, *args, **kwargs):
        cf_lambda_name = valid_cloudformation_name('utils.', cls.lambda_name)
        kwargs['ServiceToken'] = Join("",
            ["arn:aws:lambda:", Ref("AWS::Region"), ":", Ref("AWS::AccountId"),":function:", Ref(cf_lambda_name)]
        )
        depends_on = kwargs.pop('DependsOn', [])
        depends_on.append(cf_lambda_name)
        if depends_on:
            kwargs['DependsOn'] = depends_on
        return cls(*args, **kwargs)


class Sleep(BaseLambdaAWSCustomObject):
    resource_type = "Custom::Sleep"

    props = {
        'ServiceToken': (basestring, True),
        'Time': (int, True)
    }
