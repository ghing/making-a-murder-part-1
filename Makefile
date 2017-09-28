# This Makefile makes the data for the mystery.
# If you're trying to solve the mystery, you should ignore this.

DATA_DIR = data
OUTPUT_EMAIL_FILES = $(addprefix $(DATA_DIR)/emails_clean/, $(shell for i in $$(seq 0 999); do echo "$$i.txt"; done))
SUSPICIOUS_EMAIL_FILES = src/0.txt src/1.txt src/2.txt
ALL_EMAIL_FILES = $(shell ./processors/randomize_file_list.py $(OUTPUT_EMAIL_FILES) $(SUSPICIOUS_EMAIL_FILES))

.PHONY: all clean

all: $(DATA_DIR)/all_emails.pdf

$(DATA_DIR)/all_emails.pdf: $(DATA_DIR)/all_emails.txt
	cupsfilter $(DATA_DIR)/all_emails.txt > $(DATA_DIR)/all_emails.pdf

$(DATA_DIR)/all_emails.txt: $(ALL_EMAIL_FILES)
	rm -f $(DATA_DIR)/all_emails.txt && \
	for f in $?; do \
	  cat $$f >> $(DATA_DIR)/all_emails.txt; \
	  echo "" >> $(DATA_DIR)/all_emails.txt; \
	  echo "" >> $(DATA_DIR)/all_emails.txt; \
	done

$(DATA_DIR)/emails_clean/%.txt: $(DATA_DIR)/emails/%.txt
	mkdir -p $(DATA_DIR)/emails_clean && \
	cat $^ | ./processors/clean_email.py > $@

$(DATA_DIR)/emails: $(DATA_DIR)/maildir
	./processors/pick_random_emails.py $(DATA_DIR)/maildir $(DATA_DIR)/emails

$(DATA_DIR)/maildir: $(DATA_DIR)/enron_mail_20150507.tar.gz
	cd $(DATA_DIR) && \
	cp enron_mail_20150507.tar.gz enron_mail_20150507.tar.gz.bak && \
	tar zxf enron_mail_20150507.tar.gz && \
	mv enron_mail_20150507.tar.gz.bak enron_mail_20150507.tar.gz

$(DATA_DIR)/enron_mail_20150507.tar.gz: $(DATA_DIR)
	curl -L https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz \
	     --output $(DATA_DIR)/enron_mail_20150507.tar.gz

$(DATA_DIR):
	mkdir -p $(DATA_DIR)

clean:
	rm -rf $(DATA_DIR)
