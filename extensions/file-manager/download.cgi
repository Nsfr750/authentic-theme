#!/usr/bin/perl

#
# Authentic Theme (https://github.com/qooob/authentic-theme)
# Copyright Ilia Rostovtsev <programming@rostovtsev.ru>
# Copyright Alexandr Bezenkov (https://github.com/real-gecko/filemin)
# Licensed under MIT (https://github.com/qooob/authentic-theme/blob/master/LICENSE)
#

use File::Basename;
use lib (dirname(__FILE__) . '/../../lib');
use Time::Local;

require(dirname(__FILE__) . '/file-manager-lib.pm');

my $command;
my $has_zip    = has_command('zip');
my $extension  = $has_zip ? "zip" : "tar.gz";
my $filename   = $in{'filename'};
my $target_dir = tempname("$filename");
my $target     = "$target_dir/$filename.$extension";

if ($in{'cancel'} eq '1') {
    unlink_file($target_dir);
} elsif ($in{'download'} eq '1') {
    my $file = simplify_path($target);
    for $allowed_path (@allowed_paths) {
        if (is_under_directory($allowed_path, $file)) {
            my $size = -s "$target";
            print "Content-Type: application/x-download\n";
            print "Content-Disposition: attachment; filename=\"$filename.$extension\"\n";
            print "Content-Length: $size\n\n";
            open(FILE, "< $file") or die "can't open $file: $!";
            binmode FILE;
            local $/ = \102400;

            while (<FILE>) {
                print $_;
            }
            close FILE;
            unlink_file($target_dir);
            last;
        }
    }
} else {
    mkdir($target_dir, 0755);
    if ($has_zip) {
        $command = "cd " . quotemeta($cwd) . " && zip -r " . quotemeta($target);
    } else {
        $command = "tar czf " . quotemeta($target) . " -C " . quotemeta($cwd);
    }

    foreach my $name (split(/\0/, $in{'name'})) {
        $name =~ s/$in{'cwd'}\///ig;
        if (-e ($cwd . '/' . $name)) {
            $command .= " " . quotemeta($name);
        }
    }
    system_logged($command);
}
head();
