#include "utils.hpp"
#include <cmath>
#include <numeric>

namespace recommender {
namespace utils {

double cosine_similarity(const std::vector<float>& vec1, const std::vector<float>& vec2) {
    if (vec1.size() != vec2.size() || vec1.empty()) {
        return 0.0;
    }
    
    double dot = 0.0, norm1 = 0.0, norm2 = 0.0;
    for (size_t i = 0; i < vec1.size(); ++i) {
        dot += vec1[i] * vec2[i];
        norm1 += vec1[i] * vec1[i];
        norm2 += vec2[i] * vec2[i];
    }
    
    if (norm1 <= 0 || norm2 <= 0) {
        return 0.0;
    }
    
    return dot / (std::sqrt(norm1) * std::sqrt(norm2));
}

double euclidean_distance(const std::vector<float>& vec1, const std::vector<float>& vec2) {
    if (vec1.size() != vec2.size() || vec1.empty()) {
        return std::numeric_limits<double>::max();
    }
    
    double sum = 0.0;
    for (size_t i = 0; i < vec1.size(); ++i) {
        double diff = vec1[i] - vec2[i];
        sum += diff * diff;
    }
    
    return std::sqrt(sum);
}

std::vector<float> normalize_vector(const std::vector<float>& vec) {
    if (vec.empty()) {
        return vec;
    }
    
    double norm = 0.0;
    for (float v : vec) {
        norm += v * v;
    }
    norm = std::sqrt(norm);
    
    if (norm <= 0) {
        return vec;
    }
    
    std::vector<float> normalized(vec.size());
    for (size_t i = 0; i < vec.size(); ++i) {
        normalized[i] = static_cast<float>(vec[i] / norm);
    }
    
    return normalized;
}

double dot_product(const std::vector<float>& vec1, const std::vector<float>& vec2) {
    if (vec1.size() != vec2.size() || vec1.empty()) {
        return 0.0;
    }
    
    double result = 0.0;
    for (size_t i = 0; i < vec1.size(); ++i) {
        result += vec1[i] * vec2[i];
    }
    
    return result;
}

} // namespace utils
} // namespace recommender
