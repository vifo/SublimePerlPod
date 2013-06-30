#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;
use Test::More;
use File::Find;

unless ( $ENV{TEST_AUTHOR} ) {
    plan( skip_all => "Set \$ENV{TEST_AUTHOR} for CRLF/LF line endings tests" );
}

my @dirs = (
    qw(
        lib/
        bin/
        t/
        )
);
-d 'blib' and unshift @dirs, 'blib/';

find(
    {   wanted => sub {
            return unless -f;
            ok_file_has_lf_endings_only($File::Find::name);
        },
        no_chdir => 1,
    },
    @dirs
);

done_testing();

# ----------------------------------------------------------------------------
# helpers below
# ----------------------------------------------------------------------------
sub ok_file_has_lf_endings_only {
    my $filepath = shift;

    my $ok = 0;
    my $data;

    if ( open my $fh, '<', $filepath ) {
        local $/ = undef;
        $data = <$fh>;
    }
    else {
        diag sprintf "Can't open file %s for reading. %s", $filepath, $!;
    }

    $ok = ( defined $data and $data !~ m/\r\n/s );
    ok( $ok, sprintf 'File %s has LF line endings only', $filepath );
}
