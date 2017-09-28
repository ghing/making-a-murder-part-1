DATA_DIR = data

.PHONY: all clean

all: $(DATA_DIR)/connection_counts.json

$(DATA_DIR)/connection_counts.json: $(DATA_DIR)/emails_connections.ndjson
	./processors/count_connections.py < $< | \
	python -m json.tool > $@

$(DATA_DIR)/emails_connections.ndjson: $(DATA_DIR)/emails
	find $< -type f -print0 | xargs -0 -n 1 ./processors/parse_from_to.py > $@ 

$(DATA_DIR)/emails: $(DATA_DIR)/all_emails.txt
	mkdir -p $@ && \
	split -p '^Message-ID:' -a 4 $< $(DATA_DIR)/emails/email__

$(DATA_DIR)/all_emails.txt: $(DATA_DIR)/all_emails.pdf
	pdftotext -layout $< $@

clean:
	rm -rf $(DATA_DIR)/emails $(DATA_DIR)/all_emails.txt $(DATA_DIR)/emails_connections.ndjson $(DATA_DIR)/connection_counts.json
