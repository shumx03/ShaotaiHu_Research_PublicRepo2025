data_dir = "###"

base_distribution = read.csv(file.path(data_dir, "###1.csv"))
test_distribution = read.csv(file.path(data_dir, "###2.csv"))

# we will be deploying Mann-whitney-Wilcoxon U test (Wilcoxon rank-sum test)
# because we are not making any assumptions about our data, it is non-parametric

#H0: the distributions/central tendencies of base and test are identical

manw_test = function(alpha, base, test){
  n1 = length(base)
  n2 = length(test)
  
  bnt = c(base, test)
  Rall = rank(bnt)
  r_base = Rall[1:n1]
  r_test = Rall[(n1+1):(n1+n2)]
  
  Ub = sum(r_base) - (n1*(n1+1)/2)
  Ut = sum(r_test) - (n2*(n2+1)/2)
  
  Mw_stat = min(Ub, Ut)
  
  Mw_CI = c( qwilcox(alpha/2, n1, n2, lower.tail=T), qwilcox(alpha/2, n1, n2, lower.tail=F))
  pval = pwilcox(Mw_stat, n1, n2, lower.tail=T)
  
  # critical values
  # If in CI, fail to reject
  # critical/rejection region is the region outside the CI
  # If pval > alpha, fail to reject
  
  result = list(stat = Mw_stat, ci = Mw_CI, pval = pval)
  
  return(result)
}

### complete test ###
alpha = 0.00000008

for (col in colnames(base_distribution)[-1]){
  base_col = base_distribution[[col]]
  test_col = test_distribution[[col]]
  
  if (any(test_distribution[[col]] == 0)){
    cat("null ", col, "\n")
  } else {
    results = manw_test(alpha, base_col, test_col)
    cat(col, ": ", results$stat, alpha, " | ", results$ci, results$pval, "\n")
  }
}
