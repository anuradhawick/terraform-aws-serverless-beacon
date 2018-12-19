import json
import os
import queue
import threading

import boto3


SPLIT_SIZE = 1000000
PERFORM_QUERY = os.environ['PERFORM_QUERY_LAMBDA']

aws_lambda = boto3.client('lambda')


def perform_query(region, reference_bases, end_min, end_max, alternate_bases,
                  variant_type, include_details, vcf_location, responses):
    payload = json.dumps({
        'region': region,
        'reference_bases': reference_bases,
        'end_min': end_min,
        'end_max': end_max,
        'alternate_bases': alternate_bases,
        'variant_type': variant_type,
        'include_details': include_details,
        'vcf_location': vcf_location,
    })
    print("Invoking {lambda_name} with payload: {payload}".format(
        lambda_name=PERFORM_QUERY, payload=payload))
    response = aws_lambda.invoke(
        FunctionName=PERFORM_QUERY,
        Payload=payload,
    )
    response_json = response['Payload'].read()
    print("vcf_location='{vcf}', region='{region}':"
          " received payload: {payload}".format(
              vcf=vcf_location, region=region, payload=response_json))
    response_dict = json.loads(response_json)
    responses.put(response_dict)


def split_query(dataset_id, reference_name, reference_bases, region_start,
                region_end, end_min, end_max, alternate_bases, variant_type,
                include_datasets, vcf_location):
    responses = queue.Queue()
    check_all = include_datasets in ('HIT', 'ALL')
    kwargs = {
        'reference_bases': reference_bases,
        'end_min': end_min,
        'end_max': end_max,
        'alternate_bases': alternate_bases,
        'variant_type': variant_type,
        # Don't bother recording details from MISS, they'll all be 0s
        'include_details': check_all,
        'vcf_location': vcf_location,
        'responses': responses,
    }
    threads = []
    split_start = region_start
    while split_start <= region_end:
        split_end = min(split_start + SPLIT_SIZE - 1, region_end)
        kwargs['region'] = '{}:{}-{}'.format(reference_name, split_start,
                                             split_end)
        t = threading.Thread(target=perform_query,
                             kwargs=kwargs)
        t.start()
        threads.append(t)
        split_start += SPLIT_SIZE

    num_threads = len(threads)
    processed = 0
    all_alleles_count = 0
    variant_count = 0
    call_count = 0
    samples = set()
    exists = False
    while processed < num_threads and (check_all or not exists):
        response = responses.get()
        processed += 1
        if 'exists' not in response:
            # function errored out, ignore
            continue
        exists_in_split = response['exists']
        if exists_in_split:
            exists = True
            if check_all:
                all_alleles_count += response['all_alleles_count']
                variant_count += response['variant_count']
                call_count += response['call_count']
                samples.update(response['samples'])
    if (include_datasets == 'ALL' or (include_datasets == 'HIT' and exists)
            or (include_datasets == 'MISS' and not exists)):
        response_dict = {
            'include': True,
            'datasetId': dataset_id,
            'exists': exists,
            'frequency': ((all_alleles_count or call_count and None)
                          and call_count / all_alleles_count),
            'variantCount': variant_count,
            'callCount': call_count,
            'sampleCount': len(samples),
            'note': None,
            'externalUrl': None,
            'info': None,
            'error': None,
        }
    else:
        response_dict = {
            'include': False,
            'exists': exists,
        }
    return response_dict


def lambda_handler(event, context):
    print('Event Received: {}'.format(json.dumps(event)))
    dataset_id = event['dataset_id']
    reference_name = event['reference_name']
    reference_bases = event['reference_bases']
    region_start = event['region_start']
    region_end = event['region_end']
    end_min = event['end_min']
    end_max = event['end_max']
    alternate_bases = event['alternate_bases']
    variant_type = event['variant_type']
    include_datasets = event['include_datasets']
    vcf_location = event['vcf_location']
    response = split_query(
        dataset_id=dataset_id,
        reference_name=reference_name,
        reference_bases=reference_bases,
        region_start=region_start,
        region_end=region_end,
        end_min=end_min,
        end_max=end_max,
        alternate_bases=alternate_bases,
        variant_type=variant_type,
        include_datasets=include_datasets,
        vcf_location=vcf_location,
    )
    print('Returning response: {}'.format(json.dumps(response)))
    return response


