#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;
use Test::More;

unless ( $ENV{TEST_AUTHOR} ) {
    plan( skip_all => 'Set $ENV{TEST_AUTHOR} for MANIFEST tests' );
}

{
    ## no critic qw(BuiltinFunctions::ProhibitStringyEval)
    eval "use Test::CheckManifest 0.9;";
}
plan skip_all => 'Test::CheckManifest 0.9 required for MANIFEST tests' if $@;

ok_manifest();
