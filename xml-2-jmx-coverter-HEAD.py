from sys import argv
import time
import os


def get_site_urls_list(file_path):
	input = open(file_path, 'r')
	data = input.readlines()
	temp_urls = [url.replace('<url><loc>', '') for url in data if url.count('<loc>')]
	urls = []
	for temp_url in temp_urls:
		temp_list = temp_url.split('</loc>')
		for temp_item in temp_list:
			if temp_item.count('https://') and len(temp_item) < 200:
				urls.append(temp_item)

	return urls

def write_to_jmx(output, message):
	output.writelines(str(message) + '\n')


if __name__ == '__main__':
	if len(argv) < 2:
		raise AssertionError("Usage: python xml-2-jmx-coverter.py sitemap.xml thread-count start[optional] end[optional] ... ex. python xml-2-jmx-coverter.py en-ae.xml 100 500 1000")
	
	server = argv[1]
	file_path = os.path.abspath(server)
	
	thread_count = 100
	if len(argv) > 2:
		thread_count = int(argv[2])

	start = 0
	if len(argv) > 3:
		start = int(argv[3])

	urls = get_site_urls_list(file_path)
	counter = len(urls)
	
	end = len(urls) - 1
	if len(argv) > 4:
		end = int(argv[4])

	output = open(server + '.jmx', 'w')

	main_loop_counter = (end - start) / thread_count
	for temp_count in range(main_loop_counter):
		write_to_jmx(output, '      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="URLs %d:%d" enabled="true">' % (thread_count * temp_count, thread_count * (temp_count + 1)))
		write_to_jmx(output, '        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>')
		write_to_jmx(output, '        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true">')
		write_to_jmx(output, '          <boolProp name="LoopController.continue_forever">false</boolProp>')
		write_to_jmx(output, '          <intProp name="LoopController.loops">1</intProp>')
		write_to_jmx(output, '        </elementProp>')
		write_to_jmx(output, '        <stringProp name="ThreadGroup.num_threads">1</stringProp>')
		write_to_jmx(output, '        <stringProp name="ThreadGroup.ramp_time">1</stringProp>')
		write_to_jmx(output, '        <longProp name="ThreadGroup.start_time">1479725940000</longProp>')
		write_to_jmx(output, '        <longProp name="ThreadGroup.end_time">1482317940000</longProp>')
		write_to_jmx(output, '        <boolProp name="ThreadGroup.scheduler">false</boolProp>')
		write_to_jmx(output, '        <stringProp name="ThreadGroup.delay">60</stringProp>')
		write_to_jmx(output, '      </ThreadGroup>')
		write_to_jmx(output, '      <hashTree>')

		loop_start = start + (temp_count * thread_count)
		loop_end = start + (temp_count * thread_count) + thread_count
		for url in urls[loop_start:loop_end]:
			url_path = url.split('.com/')[1]
			write_to_jmx(output, '        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="HEAD %s" enabled="true">' % url_path)
			write_to_jmx(output, '          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">')
			write_to_jmx(output, '            <collectionProp name="Arguments.arguments"/>')
			write_to_jmx(output, '          </elementProp>')
			write_to_jmx(output, '          <stringProp name="HTTPSampler.domain"></stringProp>')
			write_to_jmx(output, '          <stringProp name="HTTPSampler.port"></stringProp>')
			write_to_jmx(output, '          <stringProp name="HTTPSampler.protocol"></stringProp>')
			write_to_jmx(output, '          <stringProp name="HTTPSampler.contentEncoding"></stringProp>')
			write_to_jmx(output, '          <stringProp name="HTTPSampler.path">%s</stringProp>' % url_path)
			write_to_jmx(output, '          <stringProp name="HTTPSampler.method">HEAD</stringProp>')
			write_to_jmx(output, '          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>')
			write_to_jmx(output, '          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>')
			write_to_jmx(output, '          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>')
			write_to_jmx(output, '          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>')
			write_to_jmx(output, '          <boolProp name="HTTPSampler.image_parser">true</boolProp>')
			write_to_jmx(output, '          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>')
			write_to_jmx(output, '          <stringProp name="HTTPSampler.connect_timeout"></stringProp>')
			write_to_jmx(output, '          <stringProp name="HTTPSampler.response_timeout"></stringProp>')
			write_to_jmx(output, '        </HTTPSamplerProxy>')
			write_to_jmx(output, '        <hashTree/>')	

		write_to_jmx(output, '      </hashTree>')
	
	output.close()

