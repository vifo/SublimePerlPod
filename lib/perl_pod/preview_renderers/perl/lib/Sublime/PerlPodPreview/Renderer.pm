package Sublime::PerlPodPreview::Renderer;

=encoding UTF-8

=head1 NAME

Sublime::PerlPodPreview::Renderer - Renderer helper module for Sublime Text
plugin B<Perl POD Preview>.

=cut

use 5.010001;
use strict;
use warnings;

use Carp;
use JSON;
use MIME::Base64;
use FindBin qw($Script);

=head2 read_data_from_sublime

C<< HASHREF read_data_from_sublime () >>

    my $in = read_data_from_sublime();
    # => HASHREF

Reads data passed from Sublime Text on C<STDIN>. This expects a Base64 encoded
JSON data structure on C<STDIN>, will decode it and return results as
C<HASHREF>.

Bails out with appropriate error message, if the input stream cannot be
decoded.

=cut

sub read_data_from_sublime {
    my $self = shift;

    my $in = eval {
        local $/ = undef;
        decode_json( decode_base64(<STDIN>) );
    };
    if ($@) {
        die { message => sprintf "Unable to decode JSON data from Sublime Text. JSON: %s", $@ };
    }
    unless ( exists $in->{schema_version} ) {
        die { message => sprintf 'JSON data from Sublime Text is missing required field "schema_version"' };
    }
    return $in;
}

=head2 write_data_to_sublime

C<< 1 write_data_to_sublime ( $DATA ) >>

    my $out = { rc => 0, };
    write_data_to_sublime($out);

Given a C<HASHREF> in C<$DATA>, encode data using JSON, wrap it in Base64 and
print results on C<STDOUT> for passing data back to Sublime Text.

=cut

sub write_data_to_sublime {
    my ( $self, $out ) = @_;

    croak sprintf 'Invalid arguments passed to %s::write_data_to_sublime(). Argument $OUT must be a HASHREF. '
        . 'Usage: write_data_to_sublime( $OUT )', __PACKAGE__
        unless defined $out and ref $out eq 'HASH';

    print encode_base64( encode_json($out) );
}

=head2 run

C<< noret run () >>

    # in main script
    __PACKAGE__->run;

Reads Base64 encoded JSON data from STDIN, decodes it, calls main handler and
exits.

=cut

sub run {
    my $self = shift;

    # Output, which will be send later to Sublime Text.
    my $out = {
        rc       => 0,
        messages => [],
        output   => '',
    };

    eval {
        my $in = $self->read_data_from_sublime();
        my $rc = $self->main( $in, $out );
        $out->{rc} = $rc;
    };
    if ($@) {
        my $e = $@;
        if ( ref $e eq 'HASH' ) {
            push @{ $out->{messages} }, @{ $e->{messages} } if exists $e->{messages};
            push @{ $out->{messages} }, [ 'error', $e->{message} ] if exists $e->{message};
            $out->{rc} = defined $e->{rc} ? $e->{rc} : 1;
        }
        else {
            push @{ $out->{messages} }, [ 'error', $e ];
            $out->{rc} = 1;
        }
    }

    $self->write_data_to_sublime($out);

    # Done, return final exit code.
    exit $out->{rc};
}

=head2 main

C<< INTEGER main ( $IN, $OUT ) >>

Implement main action in your script by overriding this method. C<$IN> is the
input we got from Sublime Text, C<$OUT> contains our response.

This sub must return an C<INTEGER> value, which will be used as exit code.
Returning anything else will result in failure.

=cut

sub main {
    return 0;
}

1;

__END__

=head1 AUTHOR

Victor Foitzik <vifo@cpan.org>

=head1 LICENSE AND COPYRIGHT

This software is licensed under the same terms as Perl itself.

=cut
