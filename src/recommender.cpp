#include "recommender.hpp"
#include "loader.hpp"
#include "utils.hpp"
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <algorithm>

using json = nlohmann::json;

namespace recommender {

Recommender::Recommender(const std::string& config_path) {
    std::ifstream config_file(config_path);
    if (!config_file.is_open()) {
        throw std::runtime_error("Could not open config file: " + config_path);
    }
    config_file >> config;
}

bool Recommender::initialize() {
    try {
        // Load user and item embeddings
        std::string user_emb_path = config["model_paths"]["user_embeddings"];
        std::string item_emb_path = config["model_paths"]["item_embeddings"];
        
        if (!Loader::load_embeddings(user_emb_path, user_embeddings, user_ids) ||
            !Loader::load_embeddings(item_emb_path, item_embeddings, item_ids)) {
            return false;
        }
        
        return true;
    } catch (const std::exception& e) {
        std::cerr << "Initialization error: " << e.what() << std::endl;
        return false;
    }
}

std::vector<std::string> Recommender::get_recommendations(const std::string& user_id, size_t top_k) {
    std::vector<std::pair<std::string, double>> scores;
    
    // Get user embedding
    auto user_emb = get_user_embedding(user_id);
    if (user_emb.empty()) {
        return {};
    }
    
    // Calculate similarity with all items
    for (size_t i = 0; i < item_ids.size(); ++i) {
        auto item_emb = get_item_embedding(item_ids[i]);
        double similarity = cosine_similarity(user_emb, item_emb);
        scores.emplace_back(item_ids[i], similarity);
    }
    
    // Sort by similarity (descending)
    std::sort(scores.begin(), scores.end(), 
             [](const auto& a, const auto& b) { return a.second > b.second; });
    
    // Get top-k recommendations
    std::vector<std::string> recommendations;
    size_t k = std::min(top_k, scores.size());
    for (size_t i = 0; i < k; ++i) {
        recommendations.push_back(scores[i].first);
    }
    
    return recommendations;
}

double Recommender::get_similarity(const std::string& user_id, const std::string& item_id) {
    auto user_emb = get_user_embedding(user_id);
    auto item_emb = get_item_embedding(item_id);
    
    if (user_emb.empty() || item_emb.empty()) {
        return -1.0;  // Invalid similarity
    }
    
    return cosine_similarity(user_emb, item_emb);
}

// Private helper methods
std::vector<float> Recommender::get_user_embedding(const std::string& user_id) {
    auto it = std::find(user_ids.begin(), user_ids.end(), user_id);
    if (it == user_ids.end()) {
        return {};
    }
    size_t index = std::distance(user_ids.begin(), it);
    size_t emb_size = user_embeddings.size() / user_ids.size();
    return std::vector<float>(user_embeddings.begin() + index * emb_size,
                             user_embeddings.begin() + (index + 1) * emb_size);
}

std::vector<float> Recommender::get_item_embedding(const std::string& item_id) {
    auto it = std::find(item_ids.begin(), item_ids.end(), item_id);
    if (it == item_ids.end()) {
        return {};
    }
    size_t index = std::distance(item_ids.begin(), it);
    size_t emb_size = item_embeddings.size() / item_ids.size();
    return std::vector<float>(item_embeddings.begin() + index * emb_size,
                             item_embeddings.begin() + (index + 1) * emb_size);
}

double Recommender::cosine_similarity(const std::vector<float>& vec1, const std::vector<float>& vec2) {
    if (vec1.size() != vec2.size() || vec1.empty()) {
        return 0.0;
    }
    
    double dot = 0.0;
    double norm1 = 0.0;
    double norm2 = 0.0;
    
    for (size_t i = 0; i < vec1.size(); ++i) {
        dot += vec1[i] * vec2[i];
        norm1 += vec1[i] * vec1[i];
        norm2 += vec2[i] * vec2[i];
    }
    
    if (norm1 <= 0.0 || norm2 <= 0.0) {
        return 0.0;
    }
    
    return dot / (std::sqrt(norm1) * std::sqrt(norm2));
}

} // namespace recommender
