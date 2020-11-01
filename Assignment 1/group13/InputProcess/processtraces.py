import os

location = '../traces'

traces = {
	'bzip2.log_l1misstrace': '2',
	'gcc.log_l1misstrace': '2',
	'gromacs.log_l1misstrace': '1',
	'h264ref.log_l1misstrace': '1',
	'hmmer.log_l1misstrace': '1',
	'sphinx3.log_l1misstrace': '2',
}


for trace in traces:
	numfiles = traces[trace]
	tracefiles = '{}/{}'.format(location, trace)
	outfile = '{}.text'.format(tracefiles)

	compilecommand = 'g++ readinput.cpp'
	executecommand = './a.out {} {} {}'.format(tracefiles, numfiles, outfile)

	os.system(compilecommand)
	os.system(executecommand)
	print('{}'.format(trace))
