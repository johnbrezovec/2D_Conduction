# John Brezovec 2018
# Visualization of 2-d conduction solutions

library(tidyverse)
library(viridis)

# read in the necessary files
solution <- read_csv("solution.csv")
coordinates <- read_csv("index_coordinates.csv")

# merge them
solution <- merge(coordinates, solution)

fix_symmetry <- function(s_df) {
  max_x <- max(s_df$x)
  max_y <- max(s_df$y)
  max_index <- max(s_df$index)
  # do one axis of rotation
  for (n in 1:nrow(s_df)) {
    new_row <- list(
      max_index + n,
      2 * max_x - s_df$x[n],
      s_df$y[n],
      s_df$temperature[n]
    )
    s_df[max_index + n, ] <- new_row
  }
  # do the other axis of rotation
  max_index <- max(s_df$index) # reset the max index again
  for (n in 1:nrow(s_df)) {
    new_row <- list(
      max_index + n,
      s_df$x[n],
      2 * max_y - s_df$y[n],
      s_df$temperature[n]
    )
    s_df[max_index + n, ] <- new_row
  }
  return(s_df)
}

# applying symmetry condition to create full data
solution <- fix_symmetry(solution)

# now plot
plot <- solution %>%
  ggplot(mapping = aes(x = x, y = y, color = temperature)) +
  theme_void() +
  geom_point(shape = 15, size = 1.25) +
  scale_color_viridis(option = "inferno") +
  coord_fixed()


# save the plot
ggsave("plot.png", width = 6, height = 5, bg = "transparent")
