# Test 1
#H0: Base distribution and Test distribution has the same aggregated (unweighted) mean
#HA: Base and Test has different means

# Load data
data_dir = "###"
base_distribution = read.csv(file.path(data_dir, "###1.csv"))
test_distribution = read.csv(file.path(data_dir, "###2.csv"))
cbase = base_data$loc
ctest = test_data$loc
mean_base = mean(cbase)
mean_test = mean(ctest)
nb = length(cbase)
nt = length(ctest)

# F test start
c(var(cbase), var(ctest))

# bigger over smaller
alpha = 0.05
c(var(cbase), var(ctest))
Fstat = var(ctest)/var(cbase)

pval = pf(Fstat, nt-1, nb-1, lower.tail=F) 
f_result = TRUE
if (pval < alpha){
  f_result = FALSE
  print("heterosecdastic -> unpooled")
} else {
  print("homoscedastic -> pooled")
}

xbard =  mean_base - mean_test

if (f_result == TRUE){
  # pooled
  sp2 = ((nt-1) * var(ctest) + (nb-1)*var(cbase))/(nt+nb-2)
  SE_xbar_p = sqrt(sp2)*sqrt(1/nt + 1/nb)
  tstat_p = (xbard - 0)/SE_xbar_p
  v_p = nt+nb-2
  
  pval_p = pt(abs(tstat_p), v_p, lower.tail=F)*2
  
  if (pval_p < alpha){
    print("reject H0")
  } else {
    print("fail to reject H0")
  }
  
} else if (f_result == FALSE){
  # unpooled
  SE_xbar_up = sqrt(var(ctest)/nt + var(cbase)/nb)
  tstat_up = (xbard - 0)/SE_xbar_up
  v_up = SE_xbar_up^4/(((sd(ctest))^4) / (nt^2*(nt-1)) + (sd(cbase))^4/(nb^2*(nb-1)))

  pval_up = pt(abs(tstat_up), v_up, lower.tail=F)*2
  
  if (pval_up < alpha){
    print("reject H0")
  } else {
    print("fail to reject H0")
  }
}


# Test 2 (If test 1 reject H0)
# Individual testing 

distribution_test = function(data1, data2, alpha){
  # F_test start
  if (var(data1) > var(data2)){
    Fstat = var(data1)/var(data2)
    pval = pf(Fstat, nb-1, nt-1, lower.tail=F) 
  } else if (var(data1) < var(data2)){
    Fstat = var(data2)/var(data1)
    pval = pf(Fstat, nt-1, nb-1, lower.tail=F) 
  }
  
  f_result = TRUE
  if (pval < alpha){
    f_result = FALSE
  }
  
  # t distribution testing
  xbard =  mean_base - mean_test
  
  if (f_result == TRUE){
    # pooled
    sp2 = ((nt-1) * var(data2) + (nb-1)*var(data1))/(nt+nb-2)
    SE_xbar_p = sqrt(sp2)*sqrt(1/nt + 1/nb)
    tstat_p = (xbard - 0)/SE_xbar_p
    v_p = nt+nb-2
    
    pval_p = pt(abs(tstat_p), v_p, lower.tail=F)*2
    
    if (pval_p < alpha){
      return("reject H0")
    } else {
      return("fail to reject H0")
    }
    
  } else if (f_result == FALSE){
    # unpooled
    SE_xbar_up = sqrt(var(data2)/nt + var(data1)/nb)
    tstat_up = (xbard - 0)/SE_xbar_up
    v_up = SE_xbar_up^4/(((sd(data2))^4) / (nt^2*(nt-1)) + (sd(data1))^4/(nb^2*(nb-1)))
    
    pval_up = pt(abs(tstat_up), v_up, lower.tail=F)*2
    
    if (pval_up < alpha){
      return("reject H0")
    } else {
      return("fail to reject H0")
    }
  }
}

#aggregating data for seeing output/results
base_agg = base_data
test_agg = test_data

base_agg$mean_xxx = rowMeans(base_agg[, grep("^xxx_", names(base_agg))], na.rm = TRUE)
base_agg$mean_zzz = rowMeans(base_agg[, grep("^zzz_", names(base_agg))], na.rm = TRUE)
base_agg$mean_yyy = rowMeans(base_agg[, grep("^yyy_", names(base_agg))], na.rm = TRUE)

base_agg = base_agg[, !grepl("^xxx_|^zzz_|^yyy_", names(base_agg))]

test_agg$mean_xxx = rowMeans(test_agg[, grep("^xxx_", names(test_agg))], na.rm = TRUE)
test_agg$mean_zzz = rowMeans(test_agg[, grep("^zzz_", names(test_agg))], na.rm = TRUE)
test_agg$mean_yyy = rowMeans(test_agg[, grep("^yyy_", names(test_agg))], na.rm = TRUE)

test_agg = test_agg[, !grepl("^xxx_|^zzz_|^yyy_", names(test_agg))]

base_agg <- base_agg[, -which(names(base_agg) == "other")]

for (col in colnames(base_agg)[-1]) {
    result = distribution_test(base_agg[[col]], test_agg[[col]], alpha)
    cat(col, ": ", result, "\n")
}

