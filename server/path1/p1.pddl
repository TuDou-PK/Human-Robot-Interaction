(define (problem museum-problem)
  (:domain museum-domain)
  (:objects sq-1-2 sq-1-3 sq-1-4 sq-1-5 sq-1-6 sq-1-7 
            sq-2-0 sq-2-1 sq-2-2 sq-2-3 sq-2-4 sq-2-5
            sq-2-6 sq-2-7 sq-3-3 sq-4-0 sq-4-1 sq-4-2
            sq-4-3 sq-4-4 sq-4-5 sq-4-6 sq-4-7 robot
            )

  (:init (adj sq-1-2 sq-1-3) (adj sq-1-3 sq-1-2)
         (adj sq-1-3 sq-1-4) (adj sq-1-4 sq-1-3)
         (adj sq-1-4 sq-1-5) (adj sq-1-5 sq-1-4)
         (adj sq-1-5 sq-1-6) (adj sq-1-6 sq-1-5)
 
         (adj sq-2-0 sq-2-1) (adj sq-2-1 sq-2-0)
         (adj sq-2-1 sq-2-2) (adj sq-2-2 sq-2-1)
         (adj sq-2-2 sq-2-3) (adj sq-2-3 sq-2-2)
         (adj sq-2-3 sq-2-4) (adj sq-2-4 sq-2-3)
         (adj sq-2-4 sq-2-5) (adj sq-2-5 sq-2-4)
         (adj sq-2-5 sq-2-6) (adj sq-2-6 sq-2-5)
         (adj sq-2-6 sq-2-7) (adj sq-2-7 sq-2-6)
         
         (adj sq-1-3 sq-2-3) (adj sq-2-3 sq-1-3)
         (adj sq-1-7 sq-2-7) (adj sq-2-7 sq-1-7)
         (adj sq-2-4 sq-4-4) (adj sq-4-4 sq-2-4)
         (adj sq-3-3 sq-2-3) (adj sq-2-3 sq-3-3)
         
         (adj sq-4-0 sq-4-1) (adj sq-4-1 sq-4-0)
         (adj sq-4-1 sq-4-2) (adj sq-4-2 sq-4-1)
         (adj sq-4-2 sq-4-3) (adj sq-4-3 sq-4-2)
         (adj sq-4-3 sq-4-4) (adj sq-4-4 sq-4-3)
         (adj sq-4-4 sq-4-5) (adj sq-4-5 sq-4-4)
         (adj sq-4-5 sq-4-6) (adj sq-4-6 sq-4-5)
         (adj sq-4-6 sq-4-7) (adj sq-4-7 sq-4-6)
         
         (at robot sq-3-3)
         (ro robot)
  )
  (:goal (and (at robot sq-4-7)))
)
