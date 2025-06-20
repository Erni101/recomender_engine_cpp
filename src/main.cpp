#include <iostream>
#include <string>
#include <filesystem>
#include <nlohmann/json.hpp>
#include "recommender.hpp"

namespace fs = std::filesystem;
using json = nlohmann::json;

int main(int argc, char* argv[]) {
    // Check command line arguments
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <user_id>" << std::endl;
        return 1;
    }

    // Get the directory where the executable is located
    fs::path exe_path = fs::path(argv[0]).parent_path();
    fs::path config_path = exe_path.parent_path() / "config.json";

    // Initialize recommender
    recommender::Recommender recommender(config_path.string());
    
    // Initialize with embeddings and data
    if (!recommender.initialize()) {
        std::cerr << "Failed to initialize recommender" << std::endl;
        return 1;
    }

    // Get recommendations
    std::string user_id = argv[1];
    std::vector<std::string> recommendations = recommender.get_recommendations(user_id);

    // Print results
    std::cout << "Recommendations for user " << user_id << ":" << std::endl;
    for (const auto& item : recommendations) {
        std::cout << "- " << item << std::endl;
    }

    return 0;
}
