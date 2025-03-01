// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

/*
 * Simple benchmark that runs a mixture of point lookups and inserts on ALEX.
 */

#include "../core/alex.h"

#include <iomanip>

#include "flags.h"
#include "utils.h"


// PGM library
#include "../core/pgm/pgm_index_dynamic.hpp"


// Modify these if running your own workload

// Long and Longlat Dataloads
//#define KEY_TYPE double
//#define PAYLOAD_TYPE double

// Lognormal dataload / WIKI dataset
#define KEY_TYPE int64_t
#define PAYLOAD_TYPE int64_t

// YCSB dataload
//#define KEY_TYPE uint64_t
//#define PAYLOAD_TYPE uint64_t

// Artificial new created dataloads
//#define KEY_TYPE int
//#define PAYLOAD_TYPE int

/*
 * Required flags:
 * --keys_file              path to the file that contains keys
 * --keys_file_type         file type of keys_file (options: binary or text)
 * --init_num_keys          number of keys to bulk load with
 * --total_num_keys         total number of keys in the keys file
 * --batch_size             number of operations (lookup or insert) per batch
 *
 * Optional flags:
 * --insert_frac            fraction of operations that are inserts (instead of
 * lookups)
 * --lookup_distribution    lookup keys distribution (options: uniform or zipf)
 * --time_limit             time limit, in minutes
 * --print_batch_stats      whether to output stats for each batch
 */
int main(int argc, char* argv[]) {
  auto flags = parse_flags(argc, argv);
  std::string keys_file_path = get_required(flags, "keys_file");
  std::string keys_file_type = get_required(flags, "keys_file_type");
  auto init_num_keys = stoi(get_required(flags, "init_num_keys"));
  auto total_num_keys = stoi(get_required(flags, "total_num_keys"));
  auto batch_size = stoi(get_required(flags, "batch_size"));
  auto insert_frac = stod(get_with_default(flags, "insert_frac", "0.5"));
  std::string lookup_distribution =
      get_with_default(flags, "lookup_distribution", "zipf");
  auto time_limit = stod(get_with_default(flags, "time_limit", "0.5"));
  bool print_batch_stats = get_boolean_flag(flags, "print_batch_stats");

  // Read keys from file
  auto keys = new KEY_TYPE[total_num_keys];
  if (keys_file_type == "binary") {
    load_binary_data(keys, total_num_keys, keys_file_path);
  } else if (keys_file_type == "text") {
    load_text_data(keys, total_num_keys, keys_file_path);
  } else {
    std::cerr << "--keys_file_type must be either 'binary' or 'text'"
              << std::endl;
    return 1;
  }

  
 // Combine bulk loaded keys with randomly generated payloads
 // auto values = new std::pair<KEY_TYPE, PAYLOAD_TYPE>[init_num_keys];
 // std::generate(values.begin(), values.end(), [] { return std::make_pair(std::rand(), std::rand()); });
 // std::sort(values.begin(), values.end());

    std::vector<std::pair<KEY_TYPE, PAYLOAD_TYPE>> values(init_num_keys);
    std::mt19937_64 gen_payload(std::random_device{}());
    for (int i = 0; i < init_num_keys; i++) {
      //std::cout << "iterator" << i << "  ---  init key:  "<<keys[i]<<"\n";
      values[i].first = keys[i];
      values[i].second = static_cast<PAYLOAD_TYPE>(gen_payload());
    }

    //std::generate(values.begin(), values.end(), [] { return std::make_pair(std::rand(), std::rand()); });
    std::sort(values.begin(), values.end());
    //std::cout<< "values Begin: " << values.begin() << "Values end: " << values.end()<<"\n";
 
  // Create PGM and bulk load
  pgm::DynamicPGMIndex<KEY_TYPE, PAYLOAD_TYPE> dynamic_pgm(values.begin(), values.end());
  

  // Run workload
  int i = init_num_keys;
  long long cumulative_inserts = 0;
  long long cumulative_lookups = 0;
  int num_inserts_per_batch = static_cast<int>(batch_size * insert_frac);
  int num_lookups_per_batch = batch_size - num_inserts_per_batch;
  double cumulative_insert_time = 0;
  double cumulative_lookup_time = 0;

  auto workload_start_time = std::chrono::high_resolution_clock::now();
  int batch_no = 0;
  PAYLOAD_TYPE sum = 0;
  std::cout << std::scientific;
  std::cout << std::setprecision(3);
  int debug_temp=0;
  while (true) {
    batch_no++;

    // Do lookups
    double batch_lookup_time = 0.0;
    if (i > 0) {
      KEY_TYPE* lookup_keys = nullptr;
      if (lookup_distribution == "uniform") {
        lookup_keys = get_search_keys(keys, i, num_lookups_per_batch);
      } else if (lookup_distribution == "zipf") {
        lookup_keys = get_search_keys_zipf(keys, i, num_lookups_per_batch);
      } else {
        std::cerr << "--lookup_distribution must be either 'uniform' or 'zipf'"
                  << std::endl;
        return 1;
      }
      auto lookups_start_time = std::chrono::high_resolution_clock::now();
      
      for (int j = 0; j < num_lookups_per_batch; j++) {
        KEY_TYPE key = lookup_keys[j];
        
        //PAYLOAD_TYPE* payload = dynamic_pgm.find(key);
        auto payload = dynamic_pgm.find(key);

        //if (payload) {
        //  sum += payload.K();   
        
        //}
       
      }
      

      auto lookups_end_time = std::chrono::high_resolution_clock::now();
      batch_lookup_time = std::chrono::duration_cast<std::chrono::nanoseconds>(
                              lookups_end_time - lookups_start_time)
                              .count();
      cumulative_lookup_time += batch_lookup_time;
      cumulative_lookups += num_lookups_per_batch;
      delete[] lookup_keys;
    }

    // Do inserts
    int num_actual_inserts = std::min(num_inserts_per_batch, total_num_keys - i);
    
    int num_keys_after_batch = i + num_actual_inserts;
    auto inserts_start_time = std::chrono::high_resolution_clock::now();
    for (; i < num_keys_after_batch; i++) {
      //std::cout << "iterator" << i << "  ---  insert key:  "<<keys[i]<<"\n";
      dynamic_pgm.insert_or_assign(keys[i], static_cast<PAYLOAD_TYPE>(gen_payload()));
    }
    auto inserts_end_time = std::chrono::high_resolution_clock::now();
    double batch_insert_time =
        std::chrono::duration_cast<std::chrono::nanoseconds>(inserts_end_time -
                                                             inserts_start_time)
            .count();
    cumulative_insert_time += batch_insert_time;
    cumulative_inserts += num_actual_inserts;
    debug_temp++;


    if (print_batch_stats) {
      if(batch_no==1)
        std::cout << "batch no, cumulative ops, batch lookup throughput (lookups/sec), batch insert throughput (inserts/sec), batch operation throughput (ops.sec), cumulative lookup throughput (lookups/sec), cumulative insert throughput (inserts/sec), cumulative operation throughput (ops.sec)"<< std::endl;
      int num_batch_operations = num_lookups_per_batch + num_actual_inserts;
      double batch_time = batch_lookup_time + batch_insert_time;
      long long cumulative_operations = cumulative_lookups + cumulative_inserts;
      double cumulative_time = cumulative_lookup_time + cumulative_insert_time;
      std::cout << batch_no <<","
                << cumulative_operations <<","
                << num_lookups_per_batch / batch_lookup_time * 1e9 <<","
                << num_actual_inserts / batch_insert_time * 1e9 <<","
                << num_batch_operations / batch_time * 1e9 <<","
                << cumulative_lookups / cumulative_lookup_time * 1e9 <<","
                << cumulative_inserts / cumulative_insert_time * 1e9 <<","
                << cumulative_operations / cumulative_time * 1e9 
                << std::endl;
     }

  





       /* 
      << "Batch " << batch_no
                << ", cumulative ops: " << cumulative_operations
                << "\n\tbatch throughput:\t"
                << num_lookups_per_batch / batch_lookup_time * 1e9
                << " lookups/sec,\t"
                << num_actual_inserts / batch_insert_time * 1e9
                << " inserts/sec,\t" << num_batch_operations / batch_time * 1e9
                << " ops/sec"
                << "\n\tcumulative throughput:\t"
                << cumulative_lookups / cumulative_lookup_time * 1e9
                << " lookups/sec,\t"
                << cumulative_inserts / cumulative_insert_time * 1e9
                << " inserts/sec,\t"
                << cumulative_operations / cumulative_time * 1e9 << " ops/sec"
                << std::endl;
    }

        */

    // Check for workload end conditions

    if (num_actual_inserts < num_inserts_per_batch) {
      // End if we have inserted all keys in a workload with inserts
      break;
    }
    double workload_elapsed_time =
        std::chrono::duration_cast<std::chrono::nanoseconds>(
            std::chrono::high_resolution_clock::now() - workload_start_time)
            .count();
    
    if (workload_elapsed_time > time_limit * 1e9 * 60) {
      break;
    }
  }

  //long long cumulative_operations = cumulative_lookups + cumulative_inserts;
  //double cumulative_time = cumulative_lookup_time + cumulative_insert_time;
  
 /*
  std::cout << "Cumulative stats: " << batch_no << " batches, "
            << cumulative_operations << " ops (" << cumulative_lookups
            << " lookups, " << cumulative_inserts << " inserts)"
            << "\n\tcumulative throughput:\t"
            << cumulative_lookups / cumulative_lookup_time * 1e9
            << " lookups/sec,\t"
            << cumulative_inserts / cumulative_insert_time * 1e9
            << " inserts/sec,\t"
            << cumulative_operations / cumulative_time * 1e9 << " ops/sec"
            << std::endl;
  */
 
  //delete[] keys;
  //delete[] &values;
}
