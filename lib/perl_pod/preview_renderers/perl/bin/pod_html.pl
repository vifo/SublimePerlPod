#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;

use FindBin qw($Bin);
use lib "$Bin/../lib";
use base qw(Sublime::PerlPodPreview::Renderer);
use Pod::Html;

sub main {
    my ( $self, $in, $out ) = @_;

    my $parser = Pod::Html->new( $in->{options} );
    $parser->output_string( \$out->{output} );
    $parser->parse_string_document( $in->{input} );

    return 0;
}

__PACKAGE__->run;
