#pragma once

#include <vector>
#include <cmath>
#include <algorithm>
#include <limits>
#include <nlohmann/json.hpp>

// Forward declaration for json
template<typename T> class basic_json;
using json = nlohmann::basic_json<>;

namespace recommender {

    namespace utils {
        
        // Distance metrics
        double cosine_similarity(const std::vector<float>& vec1, const std::vector<float>& vec2);
        double euclidean_distance(const std::vector<float>& vec1, const std::vector<float>& vec2);
        
        // Vector operations
        std::vector<float> normalize_vector(const std::vector<float>& vec);
        double dot_product(const std::vector<float>& vec1, const std::vector<float>& vec2);
        
        // Utility functions
        template<typename T>
        std::vector<size_t> argsort(const std::vector<T>& values, bool ascending = true) {
            std::vector<size_t> indices(values.size());
            std::iota(indices.begin(), indices.end(), 0);
            if (ascending) {
                std::sort(indices.begin(), indices.end(), 
                    [&](size_t i, size_t j) { return values[i] < values[j]; });
            } else {
                std::sort(indices.begin(), indices.end(), 
                    [&](size_t i, size_t j) { return values[i] > values[j]; });
            }
            return indices;
        }
        
        // Configuration utilities
        template<typename T>
        T get_config_value(const nlohmann::json& config, const std::string& key, const T& default_value) {
            return config.contains(key) ? config[key].get<T>() : default_value;
        }
    }
}
