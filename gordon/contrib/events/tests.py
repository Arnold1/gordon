import unittest

try:
    from mock import patch, Mock
except ImportError:
    from unittest.mock import patch, Mock

from botocore.exceptions import ClientError
from cfnresponse import SUCCESS
from gordon.utils_tests import MockContext
from .rule import rule
from .target import target


class TestContribEventsRule(unittest.TestCase):

    @patch('gordon.contrib.events.rule.rule.send')
    @patch('gordon.contrib.events.rule.rule.boto3.client')
    def test_rule_create(self, boto3_client, send_mock):
        client = Mock()
        boto3_client.return_value = client
        context = MockContext()
        event = {
            'RequestType': 'Create',
            'ResourceProperties': {
                'Name': 'rule_name',
                'ScheduleExpression': 'cron(0 20 * * ? *)',
                'State': 'ENABLED',
                'Description': 'My description',
            }
        }
        client.get_rule.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceNotFoundException'}},
            operation_name='get_rule'
        )
        client.put_rule.return_value = {'RuleArn': 'rule_arn'}

        rule.handler(event, context)

        client.put_rule.assert_called_once_with(
            Name='rule_name',
            State='ENABLED',
            ScheduleExpression='cron(0 20 * * ? *)',
            Description='My description'
        )

        send_mock.assert_called_once_with(
            event, context, SUCCESS, response_data={'Arn': 'rule_arn'}, physical_resource_id='rule-rule_name'
        )

    @patch('gordon.contrib.events.rule.rule.send')
    @patch('gordon.contrib.events.rule.rule.boto3.client')
    def test_rule_update(self, boto3_client, send_mock):
        client = Mock()
        boto3_client.return_value = client
        context = MockContext()
        event = {
            'RequestType': 'Update',
            'ResourceProperties': {
                'Name': 'rule_name',
                'ScheduleExpression': 'cron(0 20 * * ? *)',
                'State': 'ENABLED',
                'Description': 'My description',
            }
        }
        client.get_rule.return_value = True
        client.put_rule.return_value = {'RuleArn': 'rule_arn'}

        rule.handler(event, context)

        client.put_rule.assert_called_once_with(
            Name='rule_name',
            State='ENABLED',
            ScheduleExpression='cron(0 20 * * ? *)',
            Description='My description'
        )

        send_mock.assert_called_once_with(
            event, context, SUCCESS, response_data={'Arn': 'rule_arn'}, physical_resource_id='rule-rule_name'
        )

    @patch('gordon.contrib.events.rule.rule.send')
    @patch('gordon.contrib.events.rule.rule.boto3.client')
    def test_rule_delete(self, boto3_client, send_mock):
        client = Mock()
        boto3_client.return_value = client
        context = MockContext()
        event = {
            'RequestType': 'Delete',
            'ResourceProperties': {
                'Name': 'rule_name',
                'ScheduleExpression': 'cron(0 20 * * ? *)',
                'State': 'ENABLED',
                'Description': 'My description',
            }
        }
        client.get_rule.return_value = True
        client.put_rule.return_value = {'RuleArn': 'rule_arn'}

        rule.handler(event, context)

        client.put_rule.assert_not_called()
        send_mock.assert_called_once_with(
            event, context, SUCCESS
        )


class TestContribEventsTarget(unittest.TestCase):

    @patch('gordon.contrib.events.target.target.send')
    @patch('gordon.contrib.events.target.target.boto3.client')
    def test_target_create(self, boto3_client, send_mock):
        client = Mock()
        boto3_client.return_value = client
        context = MockContext()
        event = {
            'RequestType': 'Create',
            'ResourceProperties': {
                'Rule': 'rule_name',
                'Targets': [
                    {
                        'Id': 'target_0_id',
                        'Arn': 'target_0_arn',
                        'Input': 'target_0_input',
                        'InputPath': 'target_0_input_path',
                    }
                ]
            }
        }

        client.put_targets.return_value = {}

        target.handler(event, context)

        client.put_targets.assert_called_once_with(
            Rule='rule_name',
            Targets=[
                {
                    'Id': 'target_0_id',
                    'Arn': 'target_0_arn',
                    'Input': 'target_0_input',
                    'InputPath': 'target_0_input_path',
                }
            ]
        )

        send_mock.assert_called_once_with(
            event, context, SUCCESS, physical_resource_id='rule-targets-rule_name'
        )
    @patch('gordon.contrib.events.target.target.send')
    @patch('gordon.contrib.events.target.target.boto3.client')
    def test_target_update(self, boto3_client, send_mock):
        client = Mock()
        boto3_client.return_value = client
        context = MockContext()
        event = {
            'RequestType': 'Update',
            'ResourceProperties': {
                'Rule': 'rule_name',
                'Targets': [
                    {
                        'Id': 'target_0_id',
                        'Arn': 'target_0_arn',
                        'Input': 'target_0_input',
                        'InputPath': 'target_0_input_path',
                    }
                ]
            }
        }

        client.put_targets.return_value = {}
        target.handler(event, context)

        client.put_targets.assert_called_once_with(
            Rule='rule_name',
            Targets=[
                {
                    'Id': 'target_0_id',
                    'Arn': 'target_0_arn',
                    'Input': 'target_0_input',
                    'InputPath': 'target_0_input_path',
                }
            ]
        )

        send_mock.assert_called_once_with(
            event, context, SUCCESS, physical_resource_id='rule-targets-rule_name'
        )

    @patch('gordon.contrib.events.target.target.send')
    @patch('gordon.contrib.events.target.target.boto3.client')
    def test_target_delete(self, boto3_client, send_mock):
        client = Mock()
        boto3_client.return_value = client
        context = MockContext()
        event = {
            'RequestType': 'Delete',
            'ResourceProperties': {
                'Rule': 'rule_name',
                'Targets': [
                    {
                        'Id': 'target_0_id',
                        'Arn': 'target_0_arn',
                        'Input': 'target_0_input',
                        'InputPath': 'target_0_input_path',
                    }
                ]
            }
        }
        client.list_targets_by_rule.return_value = {
            'Targets': [
                {'Id': '1'},
                {'Id': '2'}
            ]
        }
        target.handler(event, context)
        client.put_targets.assert_not_called()
        client.remove_targets.assert_called_once_with(
            Rule='rule_name',
            Ids=['1', '2']
        )
        send_mock.assert_called_once_with(event, context, SUCCESS)
