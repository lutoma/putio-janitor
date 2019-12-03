import putiopy
import datetime
import yaml


def purge_old_files(client, dir_file, max_days):
	print(f'Checking "{dir_file.name}" for files older than {max_days} days')

	for file in client.File.list(parent_id=dir_file.id):
		linger_time = datetime.datetime.now() - file.created_at
		if linger_time.days > max_days:
			print(f'File {file.name} is too old ({linger_time}), deleting')
			file.delete()


def main(config):
	client = putiopy.Client(config['oauth_token'])
	root_files = client.File.list()

	for file in root_files:
		if file.name in config['public_directories']:
			purge_old_files(client, file, config['delete_after_days'])

		if file.name not in config['allowed_root_files']:
			print(f'Deleting unauthorized root file {file.name}')
			file.delete()


if __name__ == '__main__':
	with open('config.yml', 'r') as file:
		config = yaml.safe_load(file)

	main(config)
