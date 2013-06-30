#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;

use Test::More tests => 9;
use Test::Deep;

my $MODULE_NAME = 'Sublime::PerlPodPreview::Renderer';

# load module
BEGIN {
    use_ok('Sublime::PerlPodPreview::Renderer');
}

# basic module interface checks
{
    can_ok(
        $MODULE_NAME,
        qw/
            main
            read_data_from_sublime
            run
            write_data_to_sublime
            /
    );
}

# main() tests
{
    my $func = \&{ $MODULE_NAME . '::main' };
    cmp_ok( $func->(), '==', 0, 'main() works' );
}

# read_data_from_sublime() tests
{
    my $test_name = 'read_data_from_sublime() works';
    my $func      = \&{ $MODULE_NAME . '::read_data_from_sublime' };
    my $result;

    {
        my ( $error, $result );
        eval {
            local *STDIN;
            my $input = "Hello world\n";
            open STDIN, '<', \$input or die $!;
            $result = $func->($MODULE_NAME);
        };
        $error = $@;
        cmp_deeply(
            $error,
            superhashof( { message => re(qr/malformed json/i) } ),
            $test_name . ' (reports malformed JSON)'
        );
    }

    {
        my ( $error, $result );
        eval {
            local *STDIN;
            my $input = "eyAiYWN0aW9uIjogInRlc3QiIH0K";
            open STDIN, '<', \$input or die $!;
            $result = $func->($MODULE_NAME);
        };
        $error = $@;
        cmp_deeply(
            $error,
            superhashof( { message => re(qr/\"schema_version\"/i) } ),
            $test_name . ' (complains about missing "schema_version")'
        );
    }

    {
        my ( $error, $result );
        eval {
            local *STDIN;
            my $input = "eyAic2NoZW1hX3ZlcnNpb24iOiAiMS4wIiwgImFjdGlvbiI6ICJ0ZXN0IiB9Cg==";
            open STDIN, '<', \$input or die $!;
            $result = $func->($MODULE_NAME);
        };
        $error = $@;
        cmp_deeply(
            $result,
            superhashof(
                {   schema_version => "1.0",
                    action         => "test",
                }
            ),
            $test_name . ' (parses JSON)'
        );
    }
}

# write_data_to_sublime() tests
{
    my $test_name = 'write_data_to_sublime() requires/validates arguments';
    my $func      = \&{ $MODULE_NAME . '::write_data_to_sublime' };

    {
        my ( $error, $result );
        eval {
            local *STDOUT;
            my $output = '';
            open STDOUT, '>', \$output or die $!;
            $result = $func->($MODULE_NAME);
        };
        $error = $@;
        like( $error, qr/invalid arguments/i, $test_name . ' ()' );
    }

    {
        my ( $error, $result );
        eval {
            local *STDOUT;
            my $output = '';
            open STDOUT, '>', \$output or die $!;
            $result = $func->($MODULE_NAME);
        };
        $error = $@;
        like( $error, qr/invalid arguments/i, $test_name . ' ("INVALID")' );
    }

    $test_name = 'write_data_to_sublime() works';

    {
        my ( $error, $result, $output );
        $output = '';
        eval {
            local *STDOUT;
            open STDOUT, '>', \$output or die $!;
            $result = $func->( $MODULE_NAME, { rc => 0 } );
        };
        like( $output, qr/^eyJyYyI6MH0\=\r?\n$/xs, $test_name . ' ( { rc => 0 } )' );
    }
}
