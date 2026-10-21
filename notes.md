# Notes:

## Infrastructure:

1. Python notebook presentation:

- Generating the presentation

```bash
  jupyter nbconvert birds_python.ipynb --to slides --no-input --post serve
```

- Opening the presentation

```
open birds_python.slide.html
```

2.

## Statistics

### Ragav's Research questions

- Spatial range-shift type maps. Such as where the Rock Warbler was found in 1960 against where it was found in 2010.
  - One graph that shows all spottings of Rock warlblers in 1960 juxtaposed with where it was found in the 2010.

  - What has changed in the last 50 years?

- Are bird species consistenly found in one region or are they found in multiple regions?

- Enumerate the number of unique bird species in one region for each decade from 1960 - 2010.

- Closely Observe patterns of endangered bird species.
  - Obtain a list of endangered bird species from the given dataset.
  - Trends
    - Is the reporting rate of these bird species declining?
    - Number of habitats declining?
    - How varied are the diets.
  - If something showing an increasing or declining pattern. Is there any co-variate responsible for this?

- Classify species into two groups: Declining species and Increasing species.
  - Were any "increasing" species previosly present in the "declining" group and vice versa?
  - Is there anything trait (Habitat, diet, region) common about declining species?
    - Do further research on why that particular trait is in endangered?

- Association between rainfall patterns / habitat destruction.
  - Habitat destructions in NSW.
  - Rainfall patterns in NSW
    - Look at the rainfall across trends in NSW.
      - Dry regions
      - Low rainfall
      - Moderate rainfall
      - High rainfall

### Modelling:

1. Hierarchical Modelling:

- source: https://mfviz.com/hierarchical-models/

- You have a nested data, there is a categorical component to each observation in your dataset. Subject X belongs to a different group than Subject Y but you want to predict the same response variable for both the subjects.

- Consider the problem of estimating the reporting rates of small birds, but the birds have a variety of traits. Not every bird species is the same.

- Let $Y_i$ be the _response variable_ representing the predicted reporting rate for $species_i$

- Then a simple linear model to predict the $i$th bird species is defined by:

$$
Y_i = \beta_0 + \beta_1 * traits_i
$$

- One approach is to assume a different intercept for each trait:

$$
Y_i = \beta_{ij} + \beta_1 * traits_i
$$

- Where $\beta_{ij}$ is the random intercept for the ith bird in the jth trait.

- Another approach is to assume a random slope for each trait j:

$$
Y_i = beta_0 + \beta_{ij} * traits_j
$$

- Then we combine these approaches:

$$
Y_i = beta_{ij} + beta{ij} * traits_j
$$
