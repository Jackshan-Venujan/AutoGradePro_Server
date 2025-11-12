"""
Integration Helper - How to Add Performance Timing to Your Existing Code
"""

# ============================================================================
# BACKEND INTEGRATION (Django)
# ============================================================================

# Option 1: Add to your urls.py
# ------------------------------
"""
# In Server/api/urls.py

from django.urls import path
from performance_time_test.timed_views import TimedGradeSubmissionView, SingleAnswerGradingView

urlpatterns = [
    # Your existing URLs...
    
    # Add these new endpoints:
    path('grade-timed/<int:assignment_id>/', TimedGradeSubmissionView.as_view(), name='grade-timed'),
    path('grade-single/', SingleAnswerGradingView.as_view(), name='grade-single'),
]
"""

# Option 2: Patch your existing view (simpler)
# ---------------------------------------------
"""
# In Server/api/views.py

import time
import logging

logger = logging.getLogger(__name__)

class GradeSubmissionView(generics.UpdateAPIView):
    # ... existing code ...
    
    def update(self, request, *args, **kwargs):
        assignment_id = kwargs.get("assignment_id")
        
        # START TIMING - Add this line
        start_time = time.time()
        
        # Your existing grading code
        submissions = Submission.objects.filter(assignment_id=assignment_id)
        marking_scheme = get_markingScheme(assignment_id)
        if not marking_scheme:
            return Response({"error": "Marking scheme not found."}, status=404)

        scores = []
        for submission in submissions:
            total_score = grade_submission(submission, marking_scheme)
            scores.append({"id": submission.id, "score": total_score, "file_name": submission.file_name})

        # END TIMING - Add these lines
        processing_time_ms = (time.time() - start_time) * 1000
        logger.info(f"⏱️  Grading took {processing_time_ms:.2f}ms for {len(scores)} files")
        
        # Return with timing info
        return Response({
            'scores': scores,
            'processing_time_ms': round(processing_time_ms, 2)
        })
"""


# ============================================================================
# FRONTEND INTEGRATION (React)
# ============================================================================

# Step 1: Add Performance Logger Component
# ----------------------------------------
"""
// In your main layout or dashboard component
// Example: app/(dashboard)/(routes)/layout.tsx

import { PerformanceLogger } from '@/performance_time_test/performance_logger_component';

export default function DashboardLayout({ children }) {
  return (
    <div>
      <TopHeader />
      <SideNav />
      <main>
        {children}
      </main>
      
      {/* Add the Performance Logger */}
      <PerformanceLogger />
    </div>
  );
}
"""

# Step 2: Update Your API Client
# -------------------------------
"""
// In lib/api.tsx or wherever you make API calls

import { gradeAnswerWithTiming, gradeSubmissionsWithTiming } from '@/performance_time_test/grading_api_with_timing';

// Option A: Replace existing function
export const gradeAssignment = async (assignmentId: number) => {
  return await gradeSubmissionsWithTiming(assignmentId);
};

// Option B: Add timing to existing function
export const gradeAssignment = async (assignmentId: number) => {
  const startTime = performance.now();
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/grade/${assignmentId}/`, {
      method: 'PUT',
      // ... your existing config
    });
    
    const data = await response.json();
    const clientTime = performance.now() - startTime;
    
    // Log timing
    console.log(`⏱️  Grading took ${clientTime.toFixed(2)}ms`);
    
    // Log to Performance Logger component
    if (window.logGrading && data.processing_time_ms) {
      window.logGrading('batch_grading', data.processing_time_ms);
    }
    
    return data;
  } catch (error) {
    throw error;
  }
};
"""

# Step 3: Import CSS
# ------------------
"""
// In your main CSS file or globals.css
@import '../performance_time_test/performance_logger.css';
"""


# ============================================================================
# TESTING & DATA COLLECTION
# ============================================================================

# Console Quick Test
# ------------------
"""
// Open browser console (F12) and run:

// Test all question types at once
window.runPerformanceTest()

// Or test individual grading
window.gradeAnswerWithTiming({
  question_type: 'one_word',
  student_answer: 'Paris',
  correct_answer: 'Paris',
  question_text: 'What is the capital of France?',
  grading_options: { case_sensitive: false }
})
"""


# ============================================================================
# MINIMAL INTEGRATION (Just Backend Logging)
# ============================================================================

"""
If you just want server-side timing without frontend changes:

# In Server/api/functions.py - Add to is_answer_correct function

import time

def is_answer_correct(student_answer, correct_answer, grading_type, question_text="", grading_options=None):
    start_time = time.time()
    
    # ... your existing grading logic ...
    
    processing_time_ms = (time.time() - start_time) * 1000
    
    # Log to console/file
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"⏱️  {grading_type} grading: {processing_time_ms:.2f}ms")
    
    return is_correct, score, explanation

Then watch your Django console output for timing info!
"""


# ============================================================================
# EXPORTING METRICS FOR ANALYSIS
# ============================================================================

"""
1. Grade some assignments in your frontend (with Performance Logger visible)
2. Click "📥 Export Metrics" button
3. Save the JSON file (e.g., grading_performance_1234567890.json)
4. Run analysis:

   cd performance_time_test
   python collect_metrics.py grading_performance_1234567890.json

5. Use the output in your abstract!
"""

print(__doc__)
