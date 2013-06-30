#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;
use Test::More;

my $min_tpc_version = '1.08';
my $min_pc_version  = '0.18';

unless ( $ENV{TEST_AUTHOR} ) {
    plan skip_all => 'Set $ENV{TEST_AUTHOR} for POD coverage tests';
}

## no critic qw(BuiltinFunctions::ProhibitStringyEval)
eval "use Test::Pod::Coverage $min_tpc_version";
plan skip_all => "Test::Pod::Coverage $min_tpc_version required for POD coverage tests"
    if $@;

eval "use Pod::Coverage $min_pc_version";
plan skip_all => "Pod::Coverage $min_pc_version required for testing POD coverage"
    if $@;

# Don't test JSON modules.
my @modules = grep { !/^JSON/ } all_modules();
plan skip_all => 'No modules available for POD coverage tests' unless @modules;

foreach my $module_name (@modules) {
    pod_coverage_ok($module_name);
}
