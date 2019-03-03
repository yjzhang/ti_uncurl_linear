library(dplyr)
library(dynwrap)

# based on https://dynverse.org/dynwrap/articles/create_ti_method_docker.html

system("docker build -t ayuezhang27/uncurl_linear .")

ti_comp1 <- create_ti_method_container("ayuezhang27/uncurl_linear")

ncells <- 1000
pseudotime <- runif(ncells)

expression <- matrix(
  c(
    (pseudotime - 0.5) ** 2,
    sqrt(pseudotime + 20),
    pseudotime
  ),
  ncol = 3,
  dimnames = list(as.character(rep(seq_len(ncells))), as.character(c("A", "B", "C")))
)
expression <- expression + rnorm(length(expression), sd = 0.02)

start_id = rownames(expression)[which.min(pseudotime)]

counts <- round(expression)

dataset <- wrap_expression(
  expression=expression,
  counts=counts
) %>% add_prior_information(start_id=start_id)

model <- infer_trajectory(dataset, ti_comp1())
