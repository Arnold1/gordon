Gordon
=========

.. image:: https://raw.githubusercontent.com/jorgebastida/gordon/master/docs/_static/logo.png

* Preliminary doc: http://gordondoc.s3-website-eu-west-1.amazonaws.com/

Gordon is a tool to create, wire and deploy AWS Lambdas using CloudFormation in an easy way.

Usage
------
```shell
$ gordon startproject demo [--region=eu-west-1]
$ cd demo
$ gordon startapp helloworld [--runtime=py|js|java]
# ... Add helloword to demo/settings.yml installed apps.
$ gordon build
$ gordon apply [--stage=dev|prod|...]
```

Features
---------
* 100% CloudFormation resource creation.
* 100% Boilerplate free
* Python/Javascript/Java runtimes supported.
* Simple yml configuration
* Seamless integration with (``pip``,``npm`` and ``gradle``)
* Dead-simple custom multi-stage and multi region deployments ``--stage=prod``
* Supported integrations
  * Kinesis Streams
  * Dynamodb Streams
  * S3
  * CloudWatch Events
  * Apigateway
* AWS Lambda Versions an Aliases
* Dynamic stage parametrization including:
  * Environment variables
  * Jinja2 values
  * ARN translation helpers (``dynamodb-starswith://clients-``, ``dynamodb-endswith://-clients``, ``dynamodb-match://clients-`` ...)
* Extensive Documentation
* Good test suite
* Love


Why should you use this project?
-----------------------------------

Because this project doesn't introduces anything new. Gordon is a thin layer of sugar around the fact that writing CloudFormation templates sucks and some conventions around how to structure a project using Lambdas... and not much more, which is great!


Why CloudFormation?
-----------------------
One of the best advantages of using AWS is the fact that reproducibility is at it's core and their ecosystem is full of services which encourage it. Their flagship is CloudFormation.

Then... why not use plain CloudFormation? Well, there are three reasons:

1. Complexity. CloudFormation stacks are defined using JSON templates which are a nightmare to write and maintain. (Friends don't let friends write JSON files)
2. Glue. There is a lot of glue to put in between a "normal user" and the reality-check of deploying and wiring Lambda into AWS.
3. APIs. Not all AWS APIs are released when services are announced... ain't frameworks (boto3), nor integrations with CloudFormation.

This project tries to solve these three issues by:

1. Creating a really thin layer of conventions on top of easy to maintain YAML files.
2. Making everything work out of the box as well trying to make people not shoot in their foot.
3. Working around the lack of CloudFormation/Framework APIs (keeping in mind they will happen eventually)


Does gordon use gordon to deploy gordon?
-----------------------------------------
Yes, we eat our own dog food; We use gordon to create gordon. The idea is that, (unlike many other projects), we don't think streaming API commands to AWS is a nice solution, so instead, we fill the gaps with custom CloudFormation resources.

Those Custom CloudFormation resources are implemented using Lambdas (deployed by gordon)... crazy uh?!

Why all this madness? Again... because reproducibility. If you manage some resources using CloudFormation, and some others streaming API commands, when you try to reproduce or decommission your environment... you are pretty much f\*\*\*.
