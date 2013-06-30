#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;
use Test::More;

unless ( $ENV{TEST_AUTHOR} ) {
    plan( skip_all => 'Set $ENV{TEST_AUTHOR} for Perl::Critic tests' );
}

eval { require Test::Perl::Critic; };
plan skip_all => 'Test::Perl::Critic required for Perl::Critic tests'
    if $@;

my $rcfile = File::Spec->catfile( 't', '0099_perl_critic.rc' );
Test::Perl::Critic->import( -profile => $rcfile );

all_critic_ok( 'blib/bin/', 'bin/' );
