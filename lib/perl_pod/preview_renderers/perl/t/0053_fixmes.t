#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;
use Test::More;
use File::Find;

unless ( $ENV{TEST_AUTHOR} ) {
    plan skip_all => 'Set $ENV{TEST_AUTHOR} for FIXME patterns tests';
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

            return if $File::Find::name =~ m/b?lib\/JSON*/;
            return if $File::Find::name eq 't/0053_fixmes.t';

            ok_file_has_no_fixmes($File::Find::name);
        },
        no_chdir => 1,
    },
    @dirs
);

done_testing();

# ----------------------------------------------------------------------------
# helpers below
# ----------------------------------------------------------------------------
sub ok_file_has_no_fixmes {
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

    $ok = ( defined $data and $data !~ m/(FIXME|TODO|HACK)/gi );
    ok( $ok, sprintf 'File %s does not contain any FIXME patterns', $filepath );
}
