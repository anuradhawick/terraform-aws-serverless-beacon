#
# submitDataset Lambda Function
#
module "lambda-submitDataset" {
  source = "github.com/bhosking/terraform-aws-lambda"

  function_name = "submitDataset"
  description = "Creates or updates a dataset and triggers summariseVcf."
  handler = "lambda_function.lambda_handler"
  runtime = "python3.6"
  memory_size = 2048
  timeout = 5
  attach_policy = true
  policy = "${data.aws_iam_policy_document.lambda-submitDataset.json}"
  source_path = "${path.module}/lambda/submitDataset"
  reserved_concurrent_executions = -1

  environment {
    variables = {
      DATASETS_TABLE = "${aws_dynamodb_table.datasets.name}"
      SUMMARISE_DATASET_SNS_TOPIC_ARN = "${aws_sns_topic.summariseDataset.arn}"
    }
  }
}

#
# summariseDataset Lambda Function
#
module "lambda-summariseDataset" {
  source = "github.com/bhosking/terraform-aws-lambda"

  function_name = "summariseDataset"
  description = "Calculates summary counts for a dataset."
  handler = "lambda_function.lambda_handler"
  runtime = "python3.6"
  memory_size = 2048
  timeout = 10
  attach_policy = true
  policy = "${data.aws_iam_policy_document.lambda-summariseDataset.json}"
  source_path = "${path.module}/lambda/summariseDataset"
  reserved_concurrent_executions = -1

  environment {
    variables = {
      DATASETS_TABLE = "${aws_dynamodb_table.datasets.name}"
      SUMMARISE_VCF_SNS_TOPIC_ARN = "${aws_sns_topic.summariseVcf.arn}"
      VCF_SUMMARIES_TABLE = "${aws_dynamodb_table.vcf_summaries.name}"
    }
  }
}

#
# summariseVcf Lambda Function
#

module "lambda-summariseVcf" {
  source = "github.com/bhosking/terraform-aws-lambda"

  function_name = "summariseVcf"
  description = "Calculates information in a vcf and saves it in datasets dynamoDB."
  handler = "lambda_function.lambda_handler"
  runtime = "python3.6"
  memory_size = 2048
  timeout = 60
  attach_policy = true
  policy = "${data.aws_iam_policy_document.lambda-summariseVcf.json}"
  source_path = "${path.module}/lambda/summariseVcf"
  reserved_concurrent_executions = -1

  environment {
    variables = {
      SUMMARISE_SLICE_SNS_TOPIC_ARN = "${aws_sns_topic.summariseSlice.arn}"
      VCF_SUMMARIES_TABLE = "${aws_dynamodb_table.vcf_summaries.name}"
    }
  }
}

#
# summariseSlice Lambda Function
#
module "lambda-summariseSlice" {
  source = "github.com/bhosking/terraform-aws-lambda"

  function_name = "summariseSlice"
  description = "Counts calls and variants in region of a vcf."
  handler = "lambda_function.lambda_handler"
  runtime = "python3.6"
  memory_size = 2048
  timeout = 60
  attach_policy = true
  policy = "${data.aws_iam_policy_document.lambda-summariseSlice.json}"
  source_path = "${path.module}/lambda/summariseSlice"
  reserved_concurrent_executions = -1

  environment {
    variables = {
      ASSEMBLY_GSI = "${lookup(aws_dynamodb_table.datasets.global_secondary_index[0], "name")}"
      DATASETS_TABLE = "${aws_dynamodb_table.datasets.name}"
      SUMMARISE_DATASET_SNS_TOPIC_ARN = "${aws_sns_topic.summariseDataset.arn}"
      SUMMARISE_SLICE_SNS_TOPIC_ARN = "${aws_sns_topic.summariseSlice.arn}"
      VCF_SUMMARIES_TABLE = "${aws_dynamodb_table.vcf_summaries.name}"
    }
  }
}

#
# queryDatasets Lambda Function
#
module "lambda-queryDatasets" {
  source = "github.com/bhosking/terraform-aws-lambda"

  function_name = "queryDatasets"
  description = "Invokes splitQuery for each dataset and returns result."
  handler = "lambda_function.lambda_handler"
  runtime = "python3.6"
  memory_size = 2048
  timeout = 28
  attach_policy = true
  policy = "${data.aws_iam_policy_document.lambda-queryDatasets.json}"
  source_path = "${path.module}/lambda/queryDatasets"
  reserved_concurrent_executions = -1

  environment {
    variables = {
      BEACON_ID = "${var.beacon-id}"
      DATASETS_TABLE = "${aws_dynamodb_table.datasets.name}"
      SPLIT_QUERY_LAMBDA = "${module.lambda-splitQuery.function_name}"
    }
  }
}

#
# splitQuery Lambda Function
#
module "lambda-splitQuery" {
  source = "github.com/bhosking/terraform-aws-lambda"

  function_name = "splitQuery"
  description = "Splits a dataset into smaller slices of VCFs and invokes performQuery on each."
  handler = "lambda_function.lambda_handler"
  runtime = "python3.6"
  memory_size = 2048
  timeout = 26
  attach_policy = true
  policy = "${data.aws_iam_policy_document.lambda-splitQuery.json}"
  source_path = "${path.module}/lambda/splitQuery"
  reserved_concurrent_executions = -1

  environment {
    variables = {
      PERFORM_QUERY_LAMBDA = "${module.lambda-performQuery.function_name}"
    }
  }
}

#
# performQuery Lambda Function
#
module "lambda-performQuery" {
  source = "github.com/bhosking/terraform-aws-lambda"

  function_name = "performQuery"
  description = "Queries a slice of a vcf for a specified variant."
  handler = "lambda_function.lambda_handler"
  runtime = "python3.6"
  memory_size = 2048
  timeout = 24
  attach_policy = true
  policy = "${data.aws_iam_policy_document.lambda-submitDataset.json}"
  source_path = "${path.module}/lambda/submitDataset"
  reserved_concurrent_executions = -1
}
