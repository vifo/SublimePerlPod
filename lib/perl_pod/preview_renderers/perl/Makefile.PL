#!/usr/bin/env perl

use 5.010001;
use strict;
use warnings;
use ExtUtils::MakeMaker;

WriteMakefile(
    NAME             => 'Sublime::Plugin::PerlPodPreview',
    ABSTRACT         => 'External POD renderers and dependencies for Sublime Text plugin Perl POD Preview.',
    VERSION          => '0.1.0',
    MIN_PERL_VERSION => 5.010001,
    AUTHOR           => q{Victor Foitzik <vifo@cpan.org>},
    LICENSE          => 'perl',
    PL_FILES         => {},
    BUILD_REQUIRES   => {
        'Test::Pod'           => '1.48',
        'Test::Deep'          => '0.106',
        'Test::More'          => '0.94',
        'Test::CheckManifest' => '0.9'
    },
    EXE_FILES => [ 'bin/pod_text.pl', ],
    PREREQ_PM => {},
    dist      => { COMPRESS => 'gzip -9f', SUFFIX => 'gz', },
);
