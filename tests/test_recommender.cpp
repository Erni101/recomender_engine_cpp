#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "recommender.hpp"
#include "loader.hpp"
#include "utils.hpp"

// Test fixture for recommender
TEST(RecommenderTest, Initialization) {
    recommender::Recommender recommender("config.json");
    EXPECT_TRUE(recommender.initialize());
}

TEST(RecommenderTest, SimilarityCalculation) {
    // Create test embeddings
    std::vector<float> vec1 = {1.0, 0.0, 0.0};
    std::vector<float> vec2 = {0.0, 1.0, 0.0};
    
    // Test cosine similarity
    double sim = recommender::utils::cosine_similarity(vec1, vec2);
    EXPECT_DOUBLE_EQ(sim, 0.0);
}

TEST(LoaderTest, BinaryFileLoading) {
    std::vector<float> embeddings;
    std::vector<std::string> ids;
    
    // Test with a known test file
    EXPECT_TRUE(recommender::Loader::load_embeddings("test_embeddings.bin", embeddings, ids));
    
    // Verify loaded data
    EXPECT_EQ(embeddings.size(), 100);  // Example size
    EXPECT_EQ(ids.size(), 10);          // Example size
}

TEST(UtilsTest, VectorOperations) {
    std::vector<float> vec = {1.0, 2.0, 3.0};
    auto normalized = recommender::utils::normalize_vector(vec);
    
    // Verify normalization
    EXPECT_NEAR(recommender::utils::dot_product(normalized, normalized), 1.0, 1e-6);
}
