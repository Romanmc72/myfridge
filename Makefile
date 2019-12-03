# use make <command> to run these
# ensure you've installed the test dependencies from
# test_requirements.txt
test:
	# Linting tests, make it pretty
	# pip install the test_requirements.txt to run
	# or just install flake8 and run flake8
	flake8 \
	--exclude docs \
	--max-line-length 160 \
	--statistics \
	./

	# unit tests, these must work
	# or else!
	# You will have have to install
	#    pytest-cov
	# to get most of the dependencies met here
	py.test \
	--cov=food_api \
	--cov-report term-missing \
	--cov-config=.coveragerc \
	--verbose
