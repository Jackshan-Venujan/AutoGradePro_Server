/**
 * Grading API Client with Performance Timing
 * Use this instead of your regular API calls to collect timing metrics
 */

/**
 * Grade a single answer with timing measurement
 * @param {Object} answerData - The answer data to grade
 * @returns {Promise<Object>} - Grading result with timing information
 */
export const gradeAnswerWithTiming = async (answerData) => {
  const startTime = performance.now();
  
  try {
    const response = await fetch('http://localhost:8000/api/grade-single/', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}` // Adjust as needed
      },
      body: JSON.stringify(answerData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    const endTime = performance.now();
    const clientTime = endTime - startTime;
    
    // Log to console for debugging
    console.log('⏱️ Grading Performance:', {
      question_type: data.question_type,
      server_time_ms: data.processing_time_ms,
      client_total_ms: clientTime.toFixed(2),
      network_overhead_ms: (clientTime - data.processing_time_ms).toFixed(2)
    });
    
    // Log for performance logger component
    if (window.logGrading) {
      window.logGrading(data.question_type, data.processing_time_ms);
    }
    
    return data;
  } catch (error) {
    const endTime = performance.now();
    const clientTime = endTime - startTime;
    
    console.error('❌ Grading failed:', error);
    console.error(`Failed after ${clientTime.toFixed(2)}ms`);
    throw error;
  }
};

/**
 * Grade multiple submissions (batch grading) with timing
 * @param {number} assignmentId - The assignment ID
 * @returns {Promise<Object>} - Grading results with performance metrics
 */
export const gradeSubmissionsWithTiming = async (assignmentId) => {
  const startTime = performance.now();
  
  try {
    const response = await fetch(`http://localhost:8000/api/grade-timed/${assignmentId}/`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    const endTime = performance.now();
    const clientTime = endTime - startTime;
    
    // Log comprehensive metrics
    console.log('📊 Batch Grading Performance:');
    console.table({
      'Total Time (Client)': `${clientTime.toFixed(2)}ms`,
      'Total Time (Server)': `${data.performance_metrics?.total_time_ms || 0}ms`,
      'Files Processed': data.performance_metrics?.files_processed || 0,
      'Avg per File': `${data.performance_metrics?.avg_time_per_file_ms || 0}ms`
    });
    
    if (data.performance_metrics?.timing_by_type) {
      console.log('Timing by Question Type:');
      console.table(data.performance_metrics.timing_by_type);
      
      // Log individual question types to performance logger
      Object.entries(data.performance_metrics.timing_by_type).forEach(([type, stats]) => {
        if (window.logGrading && stats.avg_ms) {
          // Log each sample (using count to simulate multiple entries)
          for (let i = 0; i < Math.min(stats.count, 10); i++) {
            window.logGrading(type, stats.avg_ms);
          }
        }
      });
    }
    
    return data;
  } catch (error) {
    const endTime = performance.now();
    const clientTime = endTime - startTime;
    
    console.error('❌ Batch grading failed:', error);
    console.error(`Failed after ${clientTime.toFixed(2)}ms`);
    throw error;
  }
};

/**
 * Test grading performance for different question types
 * Use this to quickly collect sample data
 */
export const runPerformanceTest = async () => {
  console.log('🚀 Starting Performance Test...');
  console.log('This will grade sample answers to collect timing data');
  
  const testCases = [
    // One-word tests
    {
      question_type: 'one_word',
      student_answer: 'Paris',
      correct_answer: 'Paris',
      question_text: 'What is the capital of France?',
      grading_options: { case_sensitive: false }
    },
    {
      question_type: 'one_word',
      student_answer: 'Au',
      correct_answer: 'Au',
      question_text: 'What is the chemical symbol for Gold?',
      grading_options: { case_sensitive: true }
    },
    
    // List tests
    {
      question_type: 'list',
      student_answer: ['Red', 'Blue', 'Yellow'],
      correct_answer: ['Red', 'Blue', 'Yellow'],
      question_text: 'List the primary colors',
      grading_options: { 
        order_sensitive: false,
        partial_matching: true,
        case_sensitive: false
      }
    },
    
    // Numerical tests
    {
      question_type: 'numerical',
      student_answer: 3.14,
      correct_answer: 3.14,
      question_text: 'What is the value of pi (to 2 decimals)?',
      grading_options: { 
        range_sensitive: false
      }
    },
    {
      question_type: 'numerical',
      student_answer: 99.5,
      correct_answer: 100,
      question_text: 'What is the boiling point of water in Celsius?',
      grading_options: { 
        range_sensitive: true,
        tolerance_percent: 1
      }
    },
    
    // Short phrase tests (requires Ollama)
    {
      question_type: 'short_phrase',
      student_answer: 'Plants convert sunlight into energy',
      correct_answer: 'Photosynthesis is the process where plants convert sunlight into energy',
      question_text: 'What is photosynthesis?',
      grading_options: { 
        semantic_threshold: 0.7
      }
    }
  ];
  
  console.log(`Testing ${testCases.length} sample questions...`);
  
  const results = [];
  
  for (let i = 0; i < testCases.length; i++) {
    const testCase = testCases[i];
    console.log(`\n📝 Test ${i + 1}/${testCases.length}: ${testCase.question_type}`);
    
    try {
      const result = await gradeAnswerWithTiming(testCase);
      results.push({
        test_number: i + 1,
        question_type: testCase.question_type,
        processing_time_ms: result.processing_time_ms,
        is_correct: result.is_correct,
        score: result.score
      });
      
      console.log(`✅ Completed in ${result.processing_time_ms}ms`);
      
      // Small delay between tests
      await new Promise(resolve => setTimeout(resolve, 100));
    } catch (error) {
      console.error(`❌ Test ${i + 1} failed:`, error.message);
      results.push({
        test_number: i + 1,
        question_type: testCase.question_type,
        error: error.message
      });
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 Performance Test Complete');
  console.log('='.repeat(60));
  console.table(results);
  
  // Calculate summary statistics
  const byType = {};
  results.filter(r => !r.error).forEach(r => {
    if (!byType[r.question_type]) {
      byType[r.question_type] = [];
    }
    byType[r.question_type].push(r.processing_time_ms);
  });
  
  console.log('\n📈 Summary Statistics:');
  Object.entries(byType).forEach(([type, times]) => {
    const avg = times.reduce((a, b) => a + b, 0) / times.length;
    const min = Math.min(...times);
    const max = Math.max(...times);
    
    console.log(`\n${type}:`);
    console.log(`  Average: ${avg.toFixed(2)}ms`);
    console.log(`  Min: ${min.toFixed(2)}ms`);
    console.log(`  Max: ${max.toFixed(2)}ms`);
    console.log(`  Samples: ${times.length}`);
  });
  
  console.log('\n💡 Tip: Export metrics using the Performance Logger component');
  
  return results;
};

// Make available globally for easy testing in console
if (typeof window !== 'undefined') {
  window.runPerformanceTest = runPerformanceTest;
  window.gradeAnswerWithTiming = gradeAnswerWithTiming;
  window.gradeSubmissionsWithTiming = gradeSubmissionsWithTiming;
}

export default {
  gradeAnswerWithTiming,
  gradeSubmissionsWithTiming,
  runPerformanceTest
};
