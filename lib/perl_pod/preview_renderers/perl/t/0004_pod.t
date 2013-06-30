#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;
use Test::More;

my $min_tp = 1.22;
eval "use Test::Pod $min_tp";    ## no critic qw(BuiltinFunctions::ProhibitStringyEval)
plan skip_all => "Test::Pod $min_tp required for testing POD" if $@;

all_pod_files_ok();
