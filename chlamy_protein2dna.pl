#!/usr/bin/perl
# Script to convert protein seq into codon optimized dna for Chlamydomonas Reinhardtii
# Usage: chlamy_protein2dna.pl fastaFile dnaFile
# HB: 2017/07

if ($#ARGV < 1) {
	print "Usage: cr_protein2dna.pl fastaFile dnaFile\n";
}


$fasta_file = $ARGV[0];
$dna_file = $ARGV[1];

my $prot = read_fasta_file($fasta_file);

print "Codon Usage Table: http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=3055\n";
print "Sequence:\n";

my $dna = aa2dna($prot);

open (OUT, ">$dna_file") or die "can't open $dna_file: $!\n";
print OUT "$dna\n";
close OUT;

print "Done\n";

sub aa2dna {
	my ($aa) = shift;
	$aa = uc $aa;
	my (%opt_codon) = (
		'S' => 'AGC', # Serine
		'F' => 'TTC', # Phenylalanine
		'L' => 'CTG', # Leucine
		'Y' => 'TAC', # Tyrosine
		'C' => 'TGC', # Cystein
		'W' => 'TGG', # Tryptophan
		'P' => 'CCC', # Proline
		'H' => 'CAC', # Histidine
		'Q' => 'CAG', # Glutamine
		'R' => 'CGC', # Arginine
		'I' => 'ATC', # Isoleucine
		'M' => 'ATG', # Methionine
		'T' => 'ACC', # Threonine
		'N' => 'AAC', # Asparagine
		'K' => 'AAG', # Lysine
		'V' => 'GTG', # Valine
		'A' => 'GCC', # Alanine
		'D' => 'GAC', # Aspartic Acid
		'E' => 'GAG', # Glutamic Acid
		'G' => 'GGC' # Glycine
		);

	my @seq = split(//, $aa);
	my $dna = '';
	foreach $residue (@seq) {
		if(exists $opt_codon{$residue}){
			$dna = $dna . $opt_codon{$residue};
			print "$residue => $opt_codon{$residue}\n"
		} else {
			print STDERR "Unrecognized residule !!\n";
			exit;
		}
	}
	return $dna;
}

sub read_fasta_file {
   my $fasta_file = shift;
   my $seq = "";
   open (IN, $fasta_file) or die "can't open $fasta_file: $!\n";
   while (<IN>) {
      if (/>/) {
	 print "Parsing Fasta Header ...\n";
      }  else {    
         s/\s+//g; # remove whitespace
         $seq .= $_; # add sequence
      }         
   }    
   close IN; # finished with file

   return $seq;
}

