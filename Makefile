EPYDOC=epydoc  
DSTDOC=docstrings  
  
target:
	$(EPYDOC) --html --graph=all -v -o $(DSTDOC) PriceCompare/*.py  
  
clean:
	rm -rf $(DSTDOC)  

