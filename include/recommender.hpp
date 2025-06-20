#pragma once

#include <string>
#include <vector>
#include <memory>
#include <nlohmann/json.hpp>

namespace recommender {

    class Recommender {
    public:
        // Constructor
        Recommender(const std::string& config_path);
        
        // Load embeddings and data
        bool initialize();
        
        // Generate recommendations for a user
        std::vector<std::string> get_recommendations(const std::string& user_id, size_t top_k = 10);
        
        // Get similarity score between user and item
        double get_similarity(const std::string& user_id, const std::string& item_id);
        
    private:
        // Configuration
        nlohmann::json config;
        
        // Data structures
        std::vector<float> user_embeddings;
        std::vector<float> item_embeddings;
        std::vector<std::string> user_ids;
        std::vector<std::string> item_ids;
        
        // Private helper methods
        std::vector<float> get_user_embedding(const std::string& user_id);
        std::vector<float> get_item_embedding(const std::string& item_id);
        double cosine_similarity(const std::vector<float>& vec1, const std::vector<float>& vec2);
    };
}
